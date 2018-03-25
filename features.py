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

    feature_func = {
        QA_FEATURE: lambda comment: 0 if comment.answer_id > 0 else 1,
        POST_SCORE_FEATURE: lambda comment: comment.post_score,
        RUDE_WORD_FEATURE:  lambda comment: SiteCommentFeatures.word_occurrence(CommentStaticData.processed_rude_words(), comment),
        SEND_TO_SEARCH_FEATURE: lambda comment: len(SiteCommentFeatures.search_regexp.findall(comment.body)),
        WIKTIONARY_ORG_OBSCENE_WORD_FEATURE:lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.obscene_words(), comment),
        WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE:lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.abusive_words(), comment),
        WIKTIONARY_ORG_RUDE_WORD_FEATURE:   lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.rude_words(), comment),
        WIKTIONARY_ORG_IRONY_WORD_FEATURE:  lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.irony_words(), comment),
        WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE:   lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.contempt_words(), comment),
        WIKTIONARY_ORG_NEGLECT_WORD_FEATURE:    lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.neglect_words(), comment),
        WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE:lambda comment: SiteCommentFeatures.word_occurrence(WiktionaryOrg.humiliation_words(), comment)
    }

    manul_features = [
        QA_FEATURE, POST_SCORE_FEATURE, RUDE_WORD_FEATURE, SEND_TO_SEARCH_FEATURE, WIKTIONARY_ORG_OBSCENE_WORD_FEATURE,
        WIKTIONARY_ORG_ABUSIVE_WORD_FEATURE, WIKTIONARY_ORG_RUDE_WORD_FEATURE, WIKTIONARY_ORG_IRONY_WORD_FEATURE, WIKTIONARY_ORG_CONTEMPT_WORD_FEATURE,
        WIKTIONARY_ORG_NEGLECT_WORD_FEATURE, WIKTIONARY_ORG_HUMILIATION_WORD_FEATURE
    ]

    manual_feature_number = len(manul_features)
    search_regexp = re.compile("|".join(CommentStaticData.serach_links), flags=re.DOTALL)

    def __init__(self, rude_comments, 
            normal_comments, 
            textual=True, 
            manual=True, 
            wiktionary_as_dict=True, 
            use_tfidf=False, 
            use_normal_words=False, 
            verbose=False):
        self.rude_comments  = rude_comments
        self.normal_comments= normal_comments
        self.textual        = textual
        self.manual         = manual
        self.use_tfidf      = use_tfidf
        self.verbose        = verbose
        self.use_normal_words  = use_normal_words
        self.stats          = None
        self.common         = None
        self.words          = None
        self.wiktionary_as_dict = wiktionary_as_dict

        if self.verbose:
            print("[SiteCommentFeatures setup] tfidf: %s, norm/w: %s, wikti: %s" % ( str(self.use_tfidf), str(self.use_normal_words), str(self.wiktionary_as_dict) ))

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
        else:
            text = " ".join([comment.processed_body for comment in self.rude_comments])
            if self.use_normal_words:
                text += " ".join([comment.processed_body for comment in self.normal_comments])
            text = text.split(" ")
            if self.wiktionary_as_dict:
                props = WiktionaryOrg.the_props()
                for key in sorted(props):
                    text.extend(props[key]())

            self.common = collections.Counter(text).most_common()
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
            for fearure in SiteCommentFeatures.manul_features:
                result[shift+fearure] = SiteCommentFeatures.feature_func[fearure](comment)
            shift += self.manual_feature_number
        if self.wiktionary_as_dict:
            props = WiktionaryOrg.the_props()
            wikti_words = list()
            for key in sorted(props):
                wikti_words.extend(props[key]())
                

        return result

    @staticmethod
    def manual_feature_value(comment, feature):
        if feature < 0 or feature >= SiteCommentFeatures.manual_feature_number:
            return 0
        return SiteCommentFeatures.feature_func[feature](comment)

    def store(self):
        return {
            "stats": self.stats.store() if self.stats is not None else None,
            "common": self.common,
            "textual_feature_number": self.textual_feature_number,
            "textual": self.textual,
            "manual": self.manual,
            "wiktionary_as_dict": self.wiktionary_as_dict,
            "use_tfidf": self.use_tfidf,
            "use_normal_words": self.use_normal_words,
        }

    @staticmethod
    def restore(data, verbose=False):
        obj = SiteCommentFeatures(
            None, None,
            data.get('textual'),
            data.get('manual'),
            data.get('wiktionary_as_dict'),
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
    
    @staticmethod
    def word_occurrence(words, comment):
        if len(comment.processed_body.split(' ')) == 0:
            return 0
        return len([word for word in comment.processed_body.split(' ') if word in words])