# encoding:utf-8
import csv
import re
import collections
import math
import numpy as np
from operator import itemgetter
from tfidf import DocsStats, Document
from db_models import CommentStaticData
from wiktionary_org import WiktionaryOrg

class SiteCommentFeatures:
    RUDE_CLASS = 1
    NORMAL_CLASS = 0

    QA_FEATURE                  = 0 
    POST_SCORE_FEATURE          = 1 
    RUDE_WORD_FEATURE           = 2
    SEND_TO_SEARCH_FEATURE      = 3    
    WIKTIONARY_ORG_OBSCENE_WORD_FEATURE = 4
    WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE = 5
    WIKTIONARY_ORG_RUDE_WORD_FEATURE    = 6
    WIKTIONARY_ORG_IRONY_WORD_FEATURE   = 7
    WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE= 8
    WIKTIONARY_ORG_NEGLECT_WORD_FEATURE = 9
    WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE = 10
    
    manual_feature_number = 11
    feature_descs = {
        QA_FEATURE: u"Вопрос или ответ",
        POST_SCORE_FEATURE: u"Рейтинг родительского сообщения",
        RUDE_WORD_FEATURE: u"Кол–во грубых слов",
        SEND_TO_SEARCH_FEATURE: u"Отсылка к поиску",
        WIKTIONARY_ORG_OBSCENE_WORD_FEATURE: u"Кол-во матерных слов",
        WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE: u"Кол-во бранных слов",
        WIKTIONARY_ORG_RUDE_WORD_FEATURE: u"Кол-во грубых слов",
        WIKTIONARY_ORG_IRONY_WORD_FEATURE: u"Кол-во слов иронии",
        WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE: u"Кол-во слов призрения",
        WIKTIONARY_ORG_NEGLECT_WORD_FEATURE: u"Кол-во слов пренебрежения",
        WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE: u"Кол-во слов унижения"
    }

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
        pass
    
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
        def word_occurrence(words, comment):
            if len(comment.processed_body.split(' ')) == 0:
                return 0
            return sum([1 if word in words else 0 for word in comment.processed_body.split(' ')])
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
            result[shift+SiteCommentFeatures.QA_FEATURE]        = 0 if comment.answer_id > 0 else 1
            result[shift+SiteCommentFeatures.POST_SCORE_FEATURE]= comment.post_score     
            result[shift+SiteCommentFeatures.RUDE_WORD_FEATURE] = word_occurrence(CommentStaticData.processed_rude_words(), comment)
            result[shift+SiteCommentFeatures.SEND_TO_SEARCH_FEATURE]    = len(self.search_regexp.findall(comment.body))
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_OBSCENE_WORD_FEATURE]   = word_occurrence(WiktionaryOrg.obscene_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE]   = word_occurrence(WiktionaryOrg.abusive_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_RUDE_WORD_FEATURE]      = word_occurrence(WiktionaryOrg.rude_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_IRONY_WORD_FEATURE]     = word_occurrence(WiktionaryOrg.irony_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE]  = word_occurrence(WiktionaryOrg.contempt_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_NEGLECT_WORD_FEATURE]   = word_occurrence(WiktionaryOrg.neglect_words(), comment)
            result[shift+SiteCommentFeatures.WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE]   = word_occurrence(WiktionaryOrg.humiliation_words(), comment)

        return result

    def manual_feature_value(self, features, feature_id):
        shift = 0
        if self.textual:
            shift += self.textual_feature_number
        return features[shift+feature_id]

    def store(self):
        return {
            "stats": self.stats.store() if self.stats is not None else None,
            "common": self.common,
            "textual_feature_number": self.textual_feature_number,
            "textual": self.textual,
            "manual": self.manual,
            "use_tfidf": self.use_tfidf,
            "use_normal_words": self.use_normal_words,
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

        return obj

    @staticmethod
    def feature_desc(feature_id):
        return SiteCommentFeatures.feature_descs.get(feature_id)
    