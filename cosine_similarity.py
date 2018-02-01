# encoding:utf-8
import numpy as np
from operator import itemgetter

class CosineSimilarity:
    def __init__(self, documents, threshold=0.90):
        self.documents = documents
        self.threshold = threshold
        self.similar = self.similar_documents()

    def biggest_cluster(self):
        similar = self.similar

        lengths = {index: len(value) for index, value in enumerate(similar)}
        final_classes = [key for key, _ in sorted(lengths.items(), key=itemgetter(1), reverse=True)]
        return similar[final_classes[0]]

    @staticmethod
    def cosine(first, second):
        norms = float(np.linalg.norm(first.vector) * np.linalg.norm(second.vector))
        if norms != 0.:
            val = first.vector.dot(second.vector.transpose()) / norms
            return float(val[0][0])
        else:
            return 0.
    

    def similar_documents(self):
        def closest_cosine(cosines, document, threshold):
            closest = threshold
            result_index = -1
            lenght = len(cosines)
            for index in range(0, lenght):
                current_set = cosines[index]
                curr_closest = threshold
                curr_threshold = 1.
                
                for item in current_set:
                    cosin = abs(CosineSimilarity.cosine(item, document))
                    if cosin > curr_closest:
                        curr_closest = cosin
                    if cosin < curr_threshold:
                        curr_threshold = cosin
                        
                if curr_closest > closest and curr_threshold >= threshold:
                    closest = curr_closest
                    result_index = index

            return result_index
        
        result = list()    
        for document in self.documents:
            index = closest_cosine(result, document, self.threshold)
            if index < 0:
                result.append([document])
            else:
                result[index].append(document)
        
        return result

    
