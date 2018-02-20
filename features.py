# encoding:utf-8
import csv
import re
import collections
import math
import numpy as np
from operator import itemgetter
from tfidf import DocsStats, Document
from db_models import CommentStaticData

class SiteCommentFeatures:
    RUDE_CLASS = 1
    NORMAL_CLASS = 0

    POST_AUTHOR_ID_FEATURE      = 0 # 1. Post author id
    COMMENT_AUTHOR_ID_FEATURE   = 1 # 2. Comment author id
    QA_FEATURE                  = 2 # 3. Question (0) or answer (1)
    POST_SCORE_FEATURE          = 3 # 4. Post score
    RUDE_WORD_FEATURE           = 4
    SEND_TO_SEARCH_FEATURE      = 5
    
    manual_feature_number = 6

    def __init__(self, rude_comments, normal_comments, textual=True, manual=True, use_tfidf=False, use_normal_words=False, verbose=False):
        self.rude_comments  = rude_comments
        self.normal_comments= normal_comments
        self.textual        = textual
        self.manual         = manual
        self.use_tfidf      = use_tfidf
        self.verbose        = verbose
        self.use_normal_words  = use_normal_words
        self.search_regexp  = re.compile("|".join(CommentStaticData.serach_links), flags=re.DOTALL)
        self.reply_regexp   = re.compile("@[^@]+", flags=re.DOTALL)
        self.stats          = None
        self.common         = None
        self.words          = None

        if self.verbose:
            print("[SiteCommentFeatures setup] tfidf: %s, norm/w: %s" % (str(self.use_tfidf), str(self.use_normal_words)))

    def setup_tfidf(self):
        self.stats = DocsStats()
        self.docs = list()
        for comment in self.rude_comments:
            self.docs.append(
                Document(self.stats, 
                        comment.id, 
                        comment.body, 
                        comment.processed_body)
            )

        if self.use_normal_words:
            for comment in self.normal_comments:
                self.docs.append(
                    Document(self.stats, 
                            comment.id, 
                            comment.body, 
                            comment.processed_body)
                )
        self.stats.calculate_idfs()
        self.stats.vectorise_documents()
        self.tfidf_proto = self.stats.vector_proto()
        self.textual_feature_number = self.stats.dict_size()
        if self.verbose:
            print("Text feature number: %s" % (str(self.textual_feature_number)))
        
    def setup_textual(self):
        if self.use_tfidf:
            self.setup_tfidf()
            return

        text = " ".join([comment.processed_body for comment in self.rude_comments])
        if self.use_normal_words:
            text += " ".join([comment.processed_body for comment in self.normal_comments])
        self.common = collections.Counter(text.split(" ")).most_common()
        self.words = [word for word, _ in sorted(self.common)]
        self.textual_feature_number = len(self.words)
        if self.verbose:
            print("Text feature number: %s" % (str(self.textual_feature_number)))

        
    def setup_manual(self):
        total = float(len(self.rude_comments))

        self.rude_post_authors = dict()
        for comment in self.rude_comments:
            self.rude_post_authors[comment.post_author_id] = self.rude_post_authors.get(comment.post_author_id, 0) + 1
        normal_post_authors = dict()
        for comment in self.normal_comments:
            normal_post_authors[comment.post_author_id] = normal_post_authors.get(comment.post_author_id, 0) + 1

        for author in self.rude_post_authors:
            rude = float(self.rude_post_authors[author])
            normal = float(normal_post_authors.get(author, 0.))
            self.rude_post_authors[author] = rude/(rude + normal)

        self.rude_comment_authors = dict()
        for comment in self.rude_comments:
            self.rude_comment_authors[comment.author_id] = self.rude_comment_authors.get(comment.author_id, 0) + 1
        normal_comment_authors = dict()
        for comment in self.normal_comments:
            normal_comment_authors[comment.author_id] = normal_comment_authors.get(comment.author_id, 0) + 1

        for author in self.rude_comment_authors:
            rude = float(self.rude_comment_authors[author])
            normal = float(normal_comment_authors.get(author, 0.))
            self.rude_comment_authors[author] = rude/(rude + normal)

        # Переделать на нормальную калибровку (см. Флах, стр. 326)
        answers = float(len([comment for comment in self.rude_comments if comment.answer_id > 0]))
        self.question_prob = (total - answers)/total
        self.answer_prob = answers/total
        if self.verbose:
            print("Probs, ans: %s, q: %s" % (str(self.answer_prob), str(self.question_prob)))
        
        negative = float(len([comment for comment in self.rude_comments if comment.post_score <= 0]))
        self.negative_prob = negative/total
        self.positive_prob = (total-negative)/total
        if self.verbose:
            print("Probs, neg: %s, pos: %s" % (str(self.negative_prob), str(self.positive_prob)))
    
    def setup(self):
        self.setup_textual()
        self.setup_manual()

    def feature_number(self):
        feature_number = 0
        if self.textual:
            feature_number = self.textual_feature_number
        if self.manual:
            feature_number += SiteCommentFeatures.manual_feature_number
        return feature_number

    def feature(self, comment):
        shift = 0
        result = np.zeros(self.feature_number())
        if self.textual:
            if self.use_tfidf:
                document = Document(None, comment.comment_id, comment.body, comment.processed_body)
                document.process_tf()
                document.vectorise(self.tfidf_proto)
                for index, data in enumerate(document.list_result):
                    result[shift+index] = data
            else:
                common = {
                    key: value for key, value in collections.Counter(comment.processed_body.split(" ")).most_common() 
                }
                for index, word in enumerate(self.words):
                    result[shift+index] = common.get(word, 0.)
            shift += self.textual_feature_number
        if self.manual:
            result[shift+SiteCommentFeatures.POST_AUTHOR_ID_FEATURE] = (self.rude_post_authors.get(comment.post_author_id, 0.) + 1.) / (len(self.rude_post_authors) + 2)
            result[shift+SiteCommentFeatures.COMMENT_AUTHOR_ID_FEATURE] = (self.rude_comment_authors.get(comment.author_id, 0.) + 1.) / (len(self.rude_comment_authors) + 2)
            result[shift+SiteCommentFeatures.QA_FEATURE] = 0 if comment.answer_id > 0 else 1
            result[shift+SiteCommentFeatures.POST_SCORE_FEATURE] = comment.post_score 
            rude_words = CommentStaticData.processed_rude_words()
            result[shift+SiteCommentFeatures.RUDE_WORD_FEATURE] = sum([1 if word in rude_words else 0 for word in comment.processed_body.split(' ')])
            result[shift+SiteCommentFeatures.SEND_TO_SEARCH_FEATURE] = len(self.search_regexp.findall(comment.body))
            #result[shift+SiteCommentFeatures.PARSED_WORD_DICT_LEN_FEATURE] = float(len(comment.processed_body.split()))/float(len(comment.body.split()))
            #if result[shift+SiteCommentFeatures.SEND_TO_SEARCH_FEATURE] > 0:
            #    print("[Found a search link] %s" % (str(comment.body)))

        return result

    def store(self):
        return {
            "stats": self.stats.store() if self.stats is not None else None,
            "common": self.common,
            "textual_feature_number": self.textual_feature_number,
            "textual": self.textual,
            "manual": self.manual,
            "use_tfidf": self.use_tfidf,
            "use_normal_words": self.use_normal_words,
            "rude_post_authors": self.rude_post_authors,
            "rude_comment_authors": self.rude_comment_authors
        }

    @staticmethod
    def restore(data, verbose=False):
        obj = SiteCommentFeatures(
            None, None,
            data.get('textual'),
            data.get('manual'),
            data.get('use_tfidf'),
            data.get('use_normal_words'),
            verbose
        )        

        obj.stats = DocsStats.restore(data.get('stats')) if data.get('stats') is not None else None
        obj.common = data.get('common')
        obj.words = [word for word, _ in sorted(obj.common)] if obj.common is not None else None
        obj.textual_feature_number = data.get('textual_feature_number')
        obj.rude_post_authors = data.get('rude_post_authors')
        obj.rude_comment_authors = data.get('rude_comment_authors')

        return obj
