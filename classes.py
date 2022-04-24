import pandas as pd
import pickle
import math
import numpy_financial as npf
from ml import runMachineLearning

class Property:
    def __init__(self, index, data):
        self._index = index
        self.property = data.iloc[index]
        self._scheme = self.property.scheme.rstrip().title()
        self._state = self.property.state.title()
        self._district = self.property.district.title()
        self._type = self.property["property-type"].title()
        if (self.property["bldg-size"] != 0):
            self._size = self.property["bldg-size"]
        else:
            self._size = "No Information"
        self._price = self.property.price
        self._tenure = self.property["tenure-type"].title()
        self._bedroom = self.property["bedroom-num"]

    def index(self):
        return self._index
    def price(self):
        return self._price

    def showProperty(self):
        pass

    def __str__(self):
        return f'{self._scheme} Property at {self._district} RM{self._price} with {self._bedroom} rooms'


class Filter:
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

class Recommendation:
    def __init__(self, property):
        # run machine learning 
        self._property = property
        self._similarities = runMachineLearning()

    def recommendSimilar(self):
        # return similar properties
        index = self._property.index
        distances = sorted(list(enumerate(self._similarities[index])), reverse=True, key=lambda x: x[1])
        distances = distances[1:6]
        arr = [i[0] for i in distances]
        return arr

class Affordability:
    def __init__(self, property, dp, salary, pcb, loans, loanterm, interest):
        self._property = property
        self._price = property.price()
        self._downpayment = property.price() * 0.1 if (dp) else dp
        self._salary = salary
        self._pcb = pcb
        self._loans = loans
        self._loanterm = loanterm
        self._interest = interest
    
    def evalAffordability(self):
        net_income = self._salary - self._pcb
        commitment = self._loans
        maxdebt = 0.7 * net_income
        instalment = maxdebt - commitment
        maxloan = instalment * 200
        mindp = self._price - maxloan if (self._price > maxloan) else self._downpayment
        interestRate = self._interest/100 # in decimal
        period = self._loanterm * 12 # in months
        eligibleInst = math.ceil(npf.pmt(interestRate/12, period, maxloan) * -1)
        eligibility = True if (self._price < maxloan) else False
        return {"net income": net_income, "commitment": commitment, "max loan": maxloan,
                    "eligible installment": eligibleInst, "minimum downpayment": mindp, 
                    "eligibility": eligibility }
