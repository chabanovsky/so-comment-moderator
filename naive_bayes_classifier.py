# encoding:utf-8
import math
import collections
import copy

class BinaryNaiveBayesClassifier:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def train(self, rude_comments, normal_comments, fast_stats=False, only_rude_text=False, k=0.8):
        def stat_in_comments(word, comments):
            counter = 0
            for comment in comments:
                for comment_word in comment.processed_body.split(" "):
                    if word == comment_word:
                        counter +=1
                        break
            return float(counter)

        rude_border = int(k * len(rude_comments))
        normal_border = int(k * len(normal_comments))
        self.rude_train, self.rude_test = rude_comments[:rude_border], rude_comments[rude_border:]
        self.normal_train, self.normal_test = normal_comments[:normal_border], normal_comments[normal_border:]
        
        text = " ".join([comment.processed_body for comment in self.rude_train])
        if not only_rude_text:
           text += " ".join([comment.processed_body for comment in self.normal_train])
        self.common = collections.Counter(text.split(" ")).most_common()

        rude_len = float(len(rude_comments) + 2) 
        normal_len = float(len(normal_comments) + 2)

        self.rude_word_dict = { key: (stat_in_comments(key, rude_comments) + 1) / rude_len if not fast_stats else float(value + 1.)/rude_len for key, value in self.common }
        self.normal_word_dict = { key: (stat_in_comments(key, normal_comments) + 1) / normal_len if not fast_stats else float(value + 1.)/normal_len for key, value in self.common }

        self.pos_weight = 61.4
        self.neg_weight = 1.0

        total = len(self.rude_train)
        answers = float(len([comment for comment in self.rude_train if comment.answer_id > 0]))
        self.rude_question_prob = (total - answers)/total
        self.rude_answer_prob = answers/total
        if self.verbose:
            print("Probs rude, ans: %s, q: %s" % (str(self.rude_answer_prob), str(self.rude_question_prob)))
        negative = float(len([comment for comment in self.rude_train if comment.post_score <= 0]))
        self.rude_negative_prob = negative/total
        self.rude_positive_prob = (total-negative)/total
        if self.verbose:
            print("Probs (rude), neg: %s, pos: %s" % (str(self.rude_negative_prob), str(self.rude_positive_prob)))

        total = len(self.normal_train)
        answers = float(len([comment for comment in self.normal_train if comment.answer_id > 0]))
        self.normal_question_prob = (total - answers)/total
        self.normal_answer_prob = answers/total
        if self.verbose:
            print("Probs normal, ans: %s, q: %s" % (str(self.normal_answer_prob), str(self.normal_question_prob)))
        negative = float(len([comment for comment in self.normal_train if comment.post_score <= 0]))
        self.normal_negative_prob = negative/total
        self.normal_positive_prob = (total-negative)/total
        if self.verbose:
            print("Probs, neg: %s, pos: %s" % (str(self.normal_negative_prob), str(self.normal_positive_prob)))

    def adjust_weights(self):
        acc, tpr, tnr = self.current_accuracy()
        step = 0.1
        prev_tpr = tpr - 0.001

        while tpr < 0.8:
            self.pos_weight += step
            prev_tpr = tpr
            acc, tpr, tnr = self.current_accuracy()
            if self.verbose:
                print("Accuracy: %s, tpr: %s, tnr: %s" % (str(acc), str(tpr), str(tnr)) )
                self.print_params()

    def current_accuracy(self):
        rude_real, normal_real = len(self.rude_test), len(self.normal_test)
        rude_classified = sum([1 if self.classify_rude(comment) else 0 for comment in self.rude_test])
        normal_classified = sum([0 if self.classify_rude(comment) else 1 for comment in self.normal_test])
        tpr = float(rude_classified)/float(rude_real)
        tnr = float(normal_classified)/float(normal_real)
        total_objects = float(rude_real + normal_real)
        acc = (rude_real/total_objects) * tpr + (normal_real/total_objects) * tnr
        return acc, tpr, tnr

    def print_params(self):
        rude_real, normal_real = len(self.rude_test), len(self.normal_test)
        rude_classified = sum([1 if self.classify_rude(comment) else 0 for comment in self.rude_test])
        normal_classified = sum([0 if self.classify_rude(comment) else 1 for comment in self.normal_test])

        print("Total pos: %s, neg: %s" % (str(rude_real), str(normal_real)))
        print("TP: %s, FP: %s" % (str(rude_classified), str(rude_real-rude_classified)))
        print("TN: %s, FN: %s" % (str(normal_classified), str(normal_real-normal_classified)))
        print("PosWeight: %s, NegWaigt: %s" % (str(self.pos_weight), str(self.neg_weight)))


    def test(self):
        pass 
        
    def classify_rude(self, comment):
        p_rude = 0.
        p_normal = 0.
        word_array = comment.processed_body.split(" ")
        for word, _ in self.common:
            if word in word_array:
                p_rude += math.log(self.rude_word_dict[word], 10)
                p_normal += math.log(self.normal_word_dict[word], 10)
            else:
                p_rude += math.log((1 - self.rude_word_dict[word]), 10)
                p_normal += math.log((1 - self.normal_word_dict[word]), 10)

        if comment.answer_id > 0:
            p_rude += math.log(self.rude_answer_prob, 10)
            p_normal += math.log(self.normal_answer_prob, 10)
        else:
            p_rude += math.log(self.rude_question_prob, 10)
            p_normal += math.log(self.normal_question_prob, 10)

        if comment.post_score <= 0:
            p_rude += math.log(self.rude_negative_prob, 10)
            p_normal += math.log(self.normal_negative_prob, 10)
        else:
            p_rude += math.log(self.rude_positive_prob, 10)
            p_normal += math.log(self.normal_positive_prob, 10)

#        if self.verbose:
#            print ("%s, rude: %s, normal: %s\r\n\r\n" % (" ".join(word_array), str(p_rude), str(p_normal)))

        return  p_rude > p_normal