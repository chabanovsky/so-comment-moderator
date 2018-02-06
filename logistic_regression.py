# encoding:utf-8
import csv
import collections
import math
import numpy as np
from operator import itemgetter


class LogisticRegaression:
    __RudeClass = 1
    __NormalClass = 0

    def __init__(self, verbose=False, num_steps=20000, learning_rate=5e-5):
        self.verbose = verbose
        self.num_steps = num_steps 
        self.learning_rate = learning_rate

    def train(self, rude_comments, normal_comments, k=0.8):
        rude_border = int(k * len(rude_comments))
        normal_border = int(k * len(normal_comments))
        self.rude_train, self.rude_test = rude_comments[:rude_border], rude_comments[rude_border:]
        self.normal_train, self.normal_test = normal_comments[:normal_border], normal_comments[normal_border:]
            
        text = " ".join([comment.processed_body for comment in self.rude_train])
        text += " ".join([comment.processed_body for comment in self.normal_train])
        self.common = collections.Counter(text.split(" ")).most_common()
        self.words = [word for word, _ in sorted(self.common)]

        example_count = len(self.rude_train) + len(self.normal_train)
        self.features = np.zeros((example_count, len(self.words)))
        self.labels = np.zeros(example_count)

        index = 0
        for comment in self.rude_train:
            self.features[index] = self.make_feature(comment.processed_body.split(" "))
            self.labels[index] = LogisticRegaression.__RudeClass
            index += 1

        for comment in self.normal_train:
            self.features[index] = self.make_feature(comment.processed_body.split(" "))
            self.labels[index] = LogisticRegaression.__NormalClass
            index +=1   

        self.trained_weights = self.logistic_regression()

    def make_feature(self, word_array):
        result = np.zeros(len(self.words))
        common = {key: value for key, value in collections.Counter(word_array).most_common() }

        for index, word in enumerate(self.words):
            result[index] = common.get(word, 0.)

        return result

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

    def classify_rude(self, word_array):
        test = np.zeros((1, len(self.words)))
        test[0] = self.make_feature(word_array)
        scores = np.dot(test, self.trained_weights)
        preds = int(np.round(LogisticRegaression.sigmoid(scores))[0])
        return preds == LogisticRegaression.__RudeClass

    def test(self):
        rude_right = sum([1 if self.classify_rude(comment.processed_body.split(" ")) else 0 for comment in self.rude_test])
        normal_right = sum([0 if self.classify_rude(comment.processed_body.split(" ")) else 1 for comment in self.normal_test ])
        return len(self.rude_test), rude_right, len(self.normal_test), normal_right

            
