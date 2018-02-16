# encoding:utf-8
import csv
import collections
import math
import numpy as np
from operator import itemgetter
from scipy import stats
from features import SiteCommentFeatures

class LogisticRegaression:
    def __init__(self, rude_comments, normal_comments, verbose=False, k=0.8, num_steps=10000, learning_rate=5e-5):
        self.verbose = verbose
        self.num_steps = num_steps 
        self.learning_rate = learning_rate

        rude_border = int(k * len(rude_comments))
        normal_border = int(k * len(normal_comments))
        self.rude_train, self.rude_test = rude_comments[:rude_border], rude_comments[rude_border:]
        self.normal_train, self.normal_test = normal_comments[:normal_border], normal_comments[normal_border:]

        self.feature_maker = SiteCommentFeatures(self.rude_train, self.normal_train, False, True, self.verbose)
        self.feature_maker.setup()
        
    def train(self):
        example_count = len(self.rude_train) + len(self.normal_train)
        self.features = np.zeros((example_count, self.feature_maker.feature_number()))
        self.labels = np.zeros(example_count)

        index = 0
        for comment in self.rude_train:
            self.features[index] = self.feature_maker.feature(comment)
            self.labels[index] = SiteCommentFeatures.RUDE_CLASS
            index += 1

        for comment in self.normal_train:
            self.features[index] = self.feature_maker.feature(comment)
            self.labels[index] = SiteCommentFeatures.NORMAL_CLASS
            index +=1   

        self.trained_weights = self.logistic_regression()

    def log_likelihood(self, weights):
        scores = np.dot(self.features, weights)
        ll = np.sum(self.labels * scores - np.log(1 + np.exp(scores)) )
        return ll    

    @staticmethod
    def sigmoid(scores):
        return 1 / (1 + np.exp(-scores))
        
    def logistic_regression(self):
        weights = np.zeros(self.features.shape[1])
        for step in range(self.num_steps):
            scores = np.dot(self.features, weights)
            predictions = LogisticRegaression.sigmoid(scores)
            output_error_signal = self.labels - predictions
            gradient = np.dot(self.features.T, output_error_signal)
            weights += self.learning_rate * gradient
            
            if self.verbose and step % 1000 == 0:
                print(self.log_likelihood(weights))
            
        return weights    

    def classify_rude(self, comment):
        test = np.zeros((1, self.feature_maker.feature_number() ))
        test[0] = self.feature_maker.feature(comment)

        scores = np.dot(test, self.trained_weights)
        preds = int(np.round(LogisticRegaression.sigmoid(scores))[0])
        return preds == SiteCommentFeatures.RUDE_CLASS

    def test(self, print_rude_errors=False):
        rude_right = 0
        for comment in self.rude_test:
            if self.classify_rude(comment):
                rude_right +=1
            elif print_rude_errors:
                print("[Rude error] [q: %s, s: %s] [%s] %s" % (str(0 if comment.answer_id > 0 else 1), str(comment.post_score), str(comment.processed_body), str(comment.body)))
                
        normal_right = sum([0 if self.classify_rude(comment) else 1 for comment in self.normal_test ])
        return len(self.rude_test), rude_right, len(self.normal_test), normal_right

            
