# encoding:utf-8
import numpy as np

from features import SiteCommentFeatures

class SiteCommentFeatureList:
    def __init__(self, rude_comments, normal_comments, k=0.8):
        self.rude_border = int(k * len(rude_comments))
        self.normal_border = int(k * len(normal_comments))
        self.rude_train, self.rude_test = rude_comments[:self.rude_border], rude_comments[self.rude_border:]
        self.normal_train, self.normal_test = normal_comments[:self.normal_border], normal_comments[self.normal_border:]

        self.feature_maker = SiteCommentFeatures(self.rude_train, self.normal_train, True, True, False, True, True)
        self.feature_maker.setup()

    def train_set(self):
        example_count = self.rude_border + self.normal_border
        features = np.zeros((example_count, self.maker().feature_number()))
        labels = np.zeros(example_count)

        index = 0
        for comment in self.rude_train:
            features[index] = self.maker().feature(comment)
            labels[index] = SiteCommentFeatures.RUDE_CLASS
            index += 1

        for comment in self.normal_train:
            features[index] = self.feature_maker.feature(comment)
            labels[index] = SiteCommentFeatures.NORMAL_CLASS
            index +=1   

        return features, labels

    def test_set(self):
        return self.rude_test, self.normal_test

    def maker(self):
        return self.feature_maker
        
