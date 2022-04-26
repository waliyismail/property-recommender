from affordability import Affordability
from classes import propFilter
from ml import runMachineLearning
import streamlit as st
from itertools import cycle
import math, random
from property import Property
    
class App:
    def __init__(self, data):
        self._data = data
        self._states = ['Kuala Lumpur','Selangor']
        self._minPrice = data['price'].min().item()
        self._maxPrice = data['price'].max().item()
        self._propertylist = data['address'].values
        self._schemelist = sorted(data['scheme'].unique())
        self._roomlist = sorted(data['bedroom-num'].unique())
        self._typelist = sorted(data['property-type'].unique())
    
    def setStates(self):
        states = {
            # Default page.
            "page": "home",
            "rec": False,
            "eval": False,
            "selected_prop": -1,
            "affordable": -1,
        }
        return states

    def home(self):
        st.title("Property Recommender")
        st.text("A Property Recommender Website Using Machine Learning")

    def filters(self):
        # property filter form
        st.subheader("Filter your desire")
        filter_expander = st.expander("Property Filter")
        with filter_expander:
            filter_form = st.form(key='filter')
            c1,c2= filter_form.columns([1,2])
            state = c1.selectbox('State', self._states)
            schemes = c2.multiselect('Project Scheme e.g (Taman, Desa, etc )', self._schemelist, key = "scheme")
            types = filter_form.multiselect('Property Type', self._typelist, key = "type")
            rooms = filter_form.multiselect('Room Number', self._roomlist, key = "room")
            c1,c2 = filter_form.columns(2)
            minprice = c1.number_input("Minimum Price (RM)", self._minPrice, key="minprice")
            maxprice = c2.number_input("Maximum Price (RM)", self._maxPrice, key="maxprice")
            submit_button = filter_form.form_submit_button("Recommends Me Property!")
        if submit_button:
            # run filter algorithm
            fil = propFilter(state, schemes, types, rooms, minprice, maxprice)
            df = fil.filter(self._data)
            # change the data to df
            runMachineLearning(df)
            st.success("Filter Applied")

    def details(self):
        # show details of selected property
        st.session_state['page'] = 'propdetails'
        print("property details page")
        index = st.session_state['selected_prop']
        if(index != -1):
            p =  Property(index)
            with st.container():
                p.showProperty("details")
        else:
            print("index error" + str(index))

    def recommends(self, af):
        arr = random.sample(range(0,self._data.shape[0]),5)
        print("property index = " + str(st.session_state['selected_prop']))
        print(af)
        if (st.session_state['selected_prop']):
            print("similar")
            index = st.session_state['selected_prop']
            p =  Property(index)
            arr = p.similarProp(50)
            affordable = []
            if (af != -1):
               # recommends based of salary capacity
                print("not affordable")
                for i in arr:
                   pp = Property(i)
                   if (pp.price() < af):
                       affordable.append(i)
                
                if (not affordable):
                    st.write("Sorry no affordable property for you")
                else: 
                    arr = affordable
            # st.header("Top property for you")
            
        else:
            print("random")
            st.header("Top property for you")
            
        # show 4 recommended property
        cols = cycle(st.columns(4))
        
        for i in range(4):
            p = Property(arr[i])
            with next(cols):
                p.showProperty("list")

    def affordCheck(self):

        # view property details
        st.subheader("Affordability Checker")
        st.text("Simply fill up the following to check whether this property is worth for you")
        index = st.session_state['selected_prop']
        prop = Property(index)
        fr = st.form("eval-form")
        with fr:
            st.text_input("Property: ",prop.scheme() , disabled=True)
            st.text_input("Property Price (RM)",prop.price(), disabled=True)
            dp = st.number_input("Downpayment (RM) (10%)", math.ceil((10*prop.price())/100), help=prop.helpStr("dp"), key="downpayment")
            with st.container():
                st.text("Earnings and Commitment Section")
                sal = st.number_input("Monthly Gross Salary (RM)", value=2500, help=prop.helpStr("salary"), key="salary")
                pcb = st.number_input("Monthly PCB (RM)", value=330, help=prop.helpStr("pcb"), key="pcb")
                loan = st.number_input("Current Loan (RM) (Cars, Home, PTPTN, etc) ", value=450, help=prop.helpStr("loan"), key="loan")
            with st.container():
                st.text("Mortgage Details Section")
                loanterm = st.number_input("Loan Term (Years)", value=35, help=prop.helpStr("loanterm"), key="loanterm")
                rate = st.slider("Interest Rate (%)", 0.0, 20.0, 3.5, help=prop.helpStr("interest"),  key="interest")
        if fr.form_submit_button("Evaluate!"):
            afford = Affordability(prop,dp,sal,pcb,loan,loanterm,rate)
            eval = afford.evalAffordability()
            afford.showEval(eval)
            self.recommends(int(eval['max loan']))
            # st.session_state['page'] = "recommends"