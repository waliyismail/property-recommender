import streamlit as st
import pandas as pd
import pickle
# class for property
data= pd.read_csv('src/data/kl_cleaned_v2.csv')
class Property:
    def __init__(self, index):
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
    def state(self):
        return self._state
    def district(self):
        return self._district
    def size(self):
        return self._size
    def price(self):
        return self._price
    def scheme(self):
        return self._scheme
    def type(self):
        return self._type
    def tenure(self):
        return self._tenure
    def bedroom(self):
        return self._bedroom

    def showProperty(self, option):

        if(option == "details"):
            # show in more details
            print("property details page")
            st.markdown("### " + self.scheme() + " Property")
            st.markdown ('##### Price: RM' + str(self.price()))
            st.text(f'{self.district()}, {self.state()}' )
            c1, c2 = st.columns(2)
            c1.write('Property Type: ' + str(self.type()))
            c2.write('Tenure Type: ' + self.tenure())
            c1, c2 = st.columns(2)
            c1.write('Building Size (sqm): ' + str(self.size()))
            c2.write('Bedroom Number: ' + str(self.bedroom()))
            
            st.button("Evaluate Affordability", help= "Check your affordability for this property" , on_click = self.setEval)
        elif(option == "list"):
            # show in list form

            st.subheader(self.scheme() +" Property ")
            st.write('Property Type: '+ self.type())
            st.write('Bedroom Number: ' + str(self.bedroom()))
            st.write('Price: RM' + str(self.price()))
            st.button("Details",key = self.index(), on_click = self.setprop, args = (self.index(),))
        
    def helpStr(self, field):
        helpText = {
                    "dp": '10\% of property price', 
                    "salary": "Your gross salary per month",
                    "pcb": "Potongan Cukai Bulanan (income tax)",
                    "loan": "Sum of your total loans",
                    "loanterm": "How long you plan to loan",
                    "interest": "How much your bank's interest rate"
                        }
        return helpText[field]

    def setprop(self,x):
        print("set property")
        st.session_state['selected_prop'] = x
        st.session_state['page'] = "propdetails"

    def setEval(self):
        st.session_state['page'] = "affordability"

    def similarProp(self, limit):
        # return the indexes of top 50 property
        similarity = pickle.load(open('src/data/similarity.pkl','rb'))
        distances = sorted(list(enumerate(similarity[self.index()])), reverse=True, key=lambda x: x[1])
        distances = distances[1:50]
        arr = [i[0] for i in distances]
        return arr[0:limit]

    def __str__(self):
        return f'{self._scheme} Property at {self._district} RM{self._price} with {self._bedroom} rooms'
