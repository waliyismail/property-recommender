import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#read property csv file
data = pd.read_csv('src/data/kl_cleaned_v2.csv')

class ML:
    def __init__(self, data):
        self._data = data
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

# Apply clean_data function to your selected columns.
features = ['scheme', 'property-type','bedroom-num', 'price', ]

for feature in features:
    data[feature] = data[feature].apply(clean_data)

def combineField(x):
    return x['scheme'] + ' ' + x['property-type'] + ' bedroom'+ x['bedroom-num'] + ' price'+ x['price']



count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(data['desc'])

# Compute the Cosine Similarity matrix based on the count_matrix


cosine_sim = cosine_similarity(count_matrix, count_matrix)
pickle.dump(data,open('property_list.pkl','wb'))
pickle.dump(data,open('raw_property.pkl','wb'))
pickle.dump(cosine_sim,open('similarity.pkl','wb'))