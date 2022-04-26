import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class ML:
    def __init__(self, data, constraint):
        self._data = setConstraint(data, constraint)
        self._features = ['scheme', 'property-type','bedroom-num', 'price', ]

    
    def run(self):
        copydata =  self._data
        for feature in self._features:
            copydata[feature] = copydata[feature].apply(clean_data)
        
        copydata['desc'] = copydata.apply(combineField, axis=1)
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(copydata['desc'])
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        print("running machine learning")
        pickle.dump(cosine_sim,open('src/data/similarity.pkl','wb'))

def similarprop(index, k):

    similarity = pickle.load(open('src/data/similarity.pkl','rb'))
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    distances = distances[1:6]
    arr = [i[0] for i in distances]

    if (k != -1):
        for i in distances:
            p = Property(i[0], data)
            
    return arr