# encoding:utf-8
import csv
import collections
import math
import numpy as np
from operator import itemgetter
from tfidf import DocsStats, Document

class SiteCommentFeatures:
    RUDE_CLASS = 1
    NORMAL_CLASS = 0

    POST_AUTHOR_ID_FEATURE      = 0 # 1. Post author id
    COMMENT_AUTHOR_ID_FEATURE   = 1 # 2. Comment author id
    QA_FEATURE                  = 2 # 3. Question (0) or answer (1)
    POST_SCORE_FEATURE          = 3 # 4. Post score

    manual_feature_number = 4

    def __init__(self, rude_comments, normal_comments, use_tfidf=False, use_normal_words=False, verbose=False):
        self.rude_comments = rude_comments
        self.normal_comments = normal_comments
        self.use_tfidf = use_tfidf
        self.verbose = verbose
        self.use_normal_words = use_normal_words

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

    def feature_number(self, textual=True, manual=True):
        feature_number = 0
        if textual:
            feature_number = self.textual_feature_number
        if manual:
            feature_number += SiteCommentFeatures.manual_feature_number
        return feature_number

    def feature(self, comment, textual=True, manual=True):
        shift = 0
        result = np.zeros(self.feature_number(textual, manual))
        if textual:
            if self.use_tfidf:
                document = Document(None, comment.comment_id, comment.body, comment.processed_body)
                document.process_tf()
                document.vectorise(self.tfidf_proto)
                for index, data in enumerate(document.list_result):
                    result[shift+index] = data
            else:
                common = {key: value for key, value in collections.Counter(comment.processed_body.split(" ")).most_common() }
                for index, word in enumerate(self.words):
                    result[shift+index] = common.get(word, 0.)
            shift += self.textual_feature_number
        if manual:
            result[shift+SiteCommentFeatures.POST_AUTHOR_ID_FEATURE] = (self.rude_post_authors.get(comment.post_author_id, 0.) + 1.) / (len(self.rude_post_authors) + 2)
            result[shift+SiteCommentFeatures.COMMENT_AUTHOR_ID_FEATURE] = (self.rude_comment_authors.get(comment.author_id, 0.) + 1.) / (len(self.rude_comment_authors) + 2)
            result[shift+SiteCommentFeatures.QA_FEATURE] = 0 if comment.answer_id > 0 else 1 #self.answer_prob if comment.answer_id > 0 else self.question_prob
            result[shift+SiteCommentFeatures.POST_SCORE_FEATURE] = comment.post_score #self.negative_prob if comment.post_score <= 0 else self.positive_prob

        return result

