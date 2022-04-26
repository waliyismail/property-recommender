import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if field exist. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        elif isinstance(x, int):
            return str(x)
        else:
            return ''

def combineField(x):
    return x['scheme'] + ' ' + x['property-type'] + ' bedroom'+ x['bedroom-num'] + ' price'+ x['price']

# run the machine ml and save the similarity using pickle 
def runMachineLearning(data):
    ml = ML(data, {})
    ml.run()

def setConstraint(data, constraint: dict):
        #set the data from the constraint
        #apply the constraint in the dataset

        df = data
        for i in constraint:
            if( constraint[i] != -1):
                df = df[df[i] < constraint[i]]

        return df

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