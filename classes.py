class propFilter:
    def __init__(self, state, schemes, types, rooms, minprice, maxprice):
        self._state = state
        self._schemes = schemes
        self._types = types
        self._rooms = rooms
        self._minprice = minprice
        self._maxprice = maxprice

    def filter(self, data):


        df = data

        if self._schemes:
        #filter scheme
            for i in self._schemes: 
                df = df[df['scheme'] == i]

        if self._types:
            for i in self._types:
                df = df[df['property-type'] == i]
        
        if self._rooms:
            for i in self._rooms:
                df = df[df['bedroom-num'] == i]


        df = df[(df['price'] >= (self._minprice) ) & (df['price'] <= (self._maxprice))]

        return df

def filtering():
    # get all similarites indexs
    # find the associate property object
    similarity = pickle.load(open('src/data/similarity.pkl','rb'))
    distances = sorted(list(enumerate(similarity[self.index()])), reverse=True, key=lambda x: x[1])
    distances = distances[1:50]
    arr = [i[0] for i in distances]

