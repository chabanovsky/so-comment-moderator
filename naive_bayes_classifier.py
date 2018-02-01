# encoding:utf-8
import math
import collections

# Based on
# https://habrahabr.ru/post/184574/
# https://hackernoon.com/how-to-build-a-simple-spam-detecting-machine-learning-classifier-4471fe6b816e
# https://www.booleanworld.com/building-spam-filter-using-machine-learning/
class BinaryNaiveBayesClassifier:
    def __init__(self):
        pass

    def train(self, rude_comments, normal_comments, rude_cnt, normal_cnt):
        self.total      = float(rude_cnt + normal_cnt)
        self.rude_cnt   = float(rude_cnt)
        self.normal_cnt = float(normal_cnt)

        rude_full_text  = " ".join([comment.processed_body for comment in rude_comments])
        normal_full_text= " ".join([comment.processed_body for comment in normal_comments])        
        rude_common     = collections.Counter(rude_full_text.split(" ")).most_common()
        normal_common   = collections.Counter(normal_full_text.split(" ")).most_common()
        self.glued_voc_len = float(len(collections.Counter(rude_full_text + " " + normal_full_text).most_common()))

        self.total_rude_words    = float(len(rude_common))
        self.total_normal_words  = float(len(normal_common))

        self.rude_vocabulary    = { key: float(value) for key, value in rude_common }
        self.normal_vocabulary  = { key: float(value) for key, value in normal_common }

    def classify_rude(self, word_array):
        z = 1.0
        q = self.glued_voc_len
        class_value_rude = math.log(self.rude_cnt/self.total, 10)
        class_value_normal = math.log(self.normal_cnt/self.total, 10)

        p_rude = 0. #class_value_rude
        p_normal = 0. #class_value_normal
        for word in word_array:
            if len(word.replace(" ", "")) == 0:
                continue

            #print("Word: %s rude: %s, normal: %s" % (word, str(self.rude_vocabulary.get(word, 0.)), str(self.normal_vocabulary.get(word, 0.))))

            p_rude += math.log((self.rude_vocabulary.get(word, 0.) + z)/(self.total_rude_words + z*q), 10)
            p_normal += math.log((self.normal_vocabulary.get(word, 0.) + z)/(self.total_normal_words + z*q), 10)

        #print ("%s, rude: %s, normal: %s\r\n\r\n" % (" ".join(word_array), str(p_rude), str(p_normal)))

        return p_rude > p_normal