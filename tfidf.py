# encoding:utf-8
import csv
import collections
import math
import numpy as np

from utils import build_dataset

class DocsStats:
    def __init__(self):
        self.documents = list()
        self.idfs = dict()

        self.indexes = None
        self.dataset = None
        self.word_to_index = None
        self.index_to_word = None

    def add(self, document):
        if document not in self.documents:
            self.documents.append(document)

    def calculate_idfs(self):
        documents = self.documents
        doc_number = len(documents)

        full_text = " ".join([doc.filtered_text for doc in documents])
        self.indexes, self.dataset, self.word_to_index, self.index_to_word = build_dataset(full_text.split(" "))

        result = dict()
        for word, count in self.dataset:
            document_with_word_count = float(sum([1 for document in documents if document.contains(word)]))
            if document_with_word_count != 0.:
                result[word] = math.log(float(doc_number)/document_with_word_count, 10)
            else:
                result[word] = 1

        self.idfs = result   
    
    def vector_proto(self):
        vector = [(self.index_to_word[key], self.idfs[self.index_to_word[key]]) for key in sorted(self.index_to_word)]
        return vector     

    def empty_vector_proto(self):
        return np.zeros((1, len(self.dataset))) + 1

    def vector_to_words(self, vector):
        vector = vector[0].tolist()
        return [self.index_to_word[index] for index, weight in enumerate(vector) if weight > 0.]
    
    def vectorise_documents(self):
        proto = self.vector_proto()
        for document in self.documents:
            document.vectorise(proto)

    def dict_size(self):
        return len(self.dataset)

class Document:
    def __init__(self, stats, id, body, filtered_text):
        self.id     = id
        self.body   = body
        self.filtered_text  = filtered_text
        self.tfs    = self.process_tf()
        if stats is not None:
            self.stats  = stats
            self.stats.add(self)

    def process_tf(self):
        text = self.filtered_text
        words = collections.Counter(text.split(" ")).most_common()
        total_count = sum([count for word, count in words])
        return {word: float(count)/float(total_count) for word, count in words}        

    def contains(self, word):
        return self.tfs.get(word, None) != None

    def vectorise(self, vector_proto):
        result = list()
        for word, idf in vector_proto:
            if self.contains(word):
                w = self.tfs[word]
                result.append(w * idf)
            else:
                result.append(0.)

        self.list_result = result
        self.vector = np.zeros((1, len(self.list_result)))
        self.vector[0] = np.array(self.list_result)