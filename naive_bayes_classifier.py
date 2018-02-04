# encoding:utf-8
import math
import collections
import copy

class BinaryNaiveBayesClassifier:
    def __init__(self):
        pass

    def train(self, rude_comments, normal_comments):
        def stat_in_comments(word, comments):
            counter = 0
            for comment in comments:
                for comment_word in comment.processed_body.split(" "):
                    if word == comment_word:
                        counter +=1
                        break
            return float(counter)

        text = " ".join([comment.processed_body for comment in rude_comments])
        text += " ".join([comment.processed_body for comment in normal_comments])
        self.common = collections.Counter(text.split(" ")).most_common()

        rude_len = float(len(rude_comments) + 2) 
        normal_len = float(len(normal_comments) + 2)

        self.rude_word_dict = { key: (stat_in_comments(key, rude_comments) + 1) / rude_len for key, _ in self.common }
        self.normal_word_dict = { key: (stat_in_comments(key, normal_comments) + 1) / normal_len for key, _ in self.common }
        
    def classify_rude(self, word_array):
        p_rude = 0.
        p_normal = 0.
        for word, _ in self.common:
            if word in word_array:
                p_rude += math.log(self.rude_word_dict[word], 10)
                p_normal += math.log(self.normal_word_dict[word], 10)
            else:
                p_rude += math.log((1 - self.rude_word_dict[word]), 10)
                p_normal += math.log((1 - self.normal_word_dict[word]), 10)

        # print ("%s, rude: %s, normal: %s\r\n\r\n" % (" ".join(word_array), str(p_rude), str(p_normal)))

        return p_rude > p_normal