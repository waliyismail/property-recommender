from property import Property
class propFilter:
    def __init__(self, district, schemes, types, rooms, minprice, maxprice):
        self._district = district
        self._schemes = schemes
        self._types = types
        self._rooms = rooms
        self._minprice = minprice
        self._maxprice = maxprice

    def filter(self, data):

        left = []
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

    def filtering(self):
        r = 13374
        arr = []
        for i in range(r):
            p = Property(i)
            if p.scheme not in self._schemes:
                continue
            if p.bedroom() not in self._rooms:
                continue
            if p.type() not in self._types:
                continue
            if p.district() not in self._district:
                continue
            if p.price() not in range(self._minprice, self._maxprice+1):
                continue
            arr.append(i)
        return arr
        



