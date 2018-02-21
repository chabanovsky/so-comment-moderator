# encoding:utf-8
import csv
import collections
import math
import numpy as np
from operator import itemgetter
from scipy import stats

from features import SiteCommentFeatures

class LogisticRegaression:
    def __init__(self, feature_list, feature_maker, verbose=False, num_steps=50000, learning_rate=5e-5):
        self.verbose = verbose
        self.num_steps = num_steps 
        self.learning_rate = learning_rate
        self.feature_list = feature_list 
        self.feature_maker = feature_maker
        
    def train(self):
        features, labels = self.feature_list.train_set()
        self.trained_weights = self.logistic_regression(features, labels)

    def log_likelihood(self, weights, features, labels):
        scores = np.dot(features, weights)
        ll = np.sum(labels * scores - np.log(1 + np.exp(scores)) )
        return ll    

    @staticmethod
    def sigmoid(scores):
        return 1 / (1 + np.exp(-scores))
        
    def logistic_regression(self, features, labels):
        weights = np.zeros(features.shape[1])
        for step in range(self.num_steps):
            scores = np.dot(features, weights)
            predictions = LogisticRegaression.sigmoid(scores)
            output_error_signal = labels - predictions
            gradient = np.dot(features.T, output_error_signal)
            weights += self.learning_rate * gradient
            
            if self.verbose and step % 1000 == 0:
                print(self.log_likelihood(weights, features, labels))
            
        return weights    

    def classify_rude(self, comment):
        test = np.zeros((1, self.feature_maker.feature_number() ))
        test[0] = self.feature_maker.feature(comment)

        scores = np.dot(test, self.trained_weights)
        preds = int(np.round(LogisticRegaression.sigmoid(scores))[0])
        return preds == SiteCommentFeatures.RUDE_CLASS

    def test(self, print_rude_errors=False):
        rude_right = 0
        rude_test, normal_test = self.feature_list.test_set()
        for comment in rude_test:
            if self.classify_rude(comment):
                rude_right +=1
            elif print_rude_errors:
                print("[Rude error] [q: %s, s: %s] [%s] %s" % (str(0 if comment.answer_id > 0 else 1), str(comment.post_score), str(comment.processed_body), str(comment.body)))
                
        normal_right = sum([0 if self.classify_rude(comment) else 1 for comment in normal_test ])
        return len(rude_test), rude_right, len(normal_test), normal_right

    def store(self):
        return {
            "weights": self.trained_weights.tolist(),
            "num_steps": self.num_steps, 
            "learning_rate": self.learning_rate
        }

    @staticmethod
    def restore(data, feature_maker, verbose=True):
        logreg = LogisticRegaression(None, feature_maker, verbose, data.get("num_steps"), data.get("learning_rate"))
        logreg.trained_weights = np.array(data.get("weights"))

        return logreg
            
