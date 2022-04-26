from ml import runMachineLearning
import streamlit as st
from persist import persist
from itertools import cycle
import math, random
import PIL as Image
import pickle
from classes import Property, Affordability, Recommendation
from ml import ML
def setprop(x):
    print("set prop")
    st.session_state['selected_prop'] = x
    st.session_state['page'] = "propdetails"

def setEval():
    st.session_state['page'] = "affordability"

def similarprop(index, k):

    similarity = pickle.load(open('src/data/similarity.pkl','rb'))
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    distances = distances[1:6]
    arr = [i[0] for i in distances]

    if (k != -1):
        for i in distances:
            p = Property(i[0], data)
            
    return arr

def showEval(eval):
    st.success("Evaluation Report successfully created" )
    st.subheader("Affordability Evaluation Report")

    with st.container():
        st.text_input("Monthly Net Income: ", "RM" + eval['net income'], disabled=True)
        st.text_input("Monthly Commitment: ", "RM" + eval['commitment'], disabled=True)
        c1,c2= st.columns(2)
        c1.text_input("Loan Required: ", "RM" + eval["max loan"], disabled=True)
        c2.text_input("Max Eligible Loan: ", "RM" + eval["max loan"], disabled=True)
        c1,c2= st.columns(2)
        c1.text_input("Monthly Installment Required: ", "RM" + eval["eligible installment"], disabled=True)
        c2.text_input("Affordable Monthly Installment: ", "RM" + eval["eligible installment"], disabled=True)
        st.text_input("Minimum Downpayment Required:", "RM" + eval["min downpayment"], disabled=True)
    
    with st.container():
        st.subheader("Overall Recommendations")
        if (eval['eligibility']):
            st.text("This property is affordable by you")
            st.text(f"You can still own a higher value property up to your max loan amount (RM{eval['max loan']})")
        else:
            st.text("This property is not affordable by you")
            st.text(f"In order to own this property you need to prepare higher downpayment (RM{eval['min downpayment']})")
            st.text(f"Try finding property below your max loan (RM{eval['max loan']})")
        
    with st.container():
        # find property below max loan
        st.text("Consider these property below")
        # set affordable property page
        st.session_state['filter_price'] = True
    
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
            "selected_prop": 0,
        }
        return states

    def home(self):
        st.title("Property Recommender")
        st.text("A Property Recommender Website Using Machine Learning")

    def filters(self):
        st.subheader("Filter your desire")
        filter_expander = st.expander("Property Filter")
        with filter_expander:
            filter_form = st.form(key='filter')
            c1,c2= filter_form.columns([1,2])
            c1.selectbox('State', self._states)
            c2.multiselect('Project Scheme e.g (Taman, Desa, etc )', self._schemelist, key = "scheme")
            filter_form.multiselect('Property Type', self._typelist, key = "type")
            filter_form.multiselect('Room Number', self._roomlist, key = "room")
            c1,c2 = filter_form.columns(2)
            c1.number_input("Minimum Price (RM)", self._minPrice, key="minprice")
            c2.number_input("Maximum Price (RM)", self._maxPrice, key="maxprice")
            submit_button = filter_form.form_submit_button("Recommends Me Property!")
        if submit_button:
            st.success("Filter Applied")

    def details(self):
        # show details of selected property
        st.session_state['page'] = 'propdetails'
        print("property details page")
        with st.container():
            index = st.session_state['selected_prop']
            st.session_state['page'] = 'home'
            randpic = random.randint(1,3)
            p = Property(index, self._data)
            ptype = p.property.type +"/" + str(randpic)
            imgpath = "src/images/" + ptype + ".jpg"
            # img = Image.open(imgpath)
            # st.image(img, width =500)
            st.markdown("### " + p.scheme() + " Property")
            st.markdown ('##### Price: RM' + str(p.price()))
            st.text(f'{p.district()}, {p.state()}' )
            c1, c2 = st.columns(2)
            c1.write('Property Type: ' + str(p.type()))
            c2.write('Tenure Type: ' + p.tenure())
            c1, c2 = st.columns(2)
            c1.write('Building Size (sqm): ' + str(p.size()))
            c2.write('Bedroom Number: ' + str(p.bedroom()))
            
            st.button("Evaluate Affordability", help= "Check your affordability for this property" , on_click = setEval)



    def recommends(self , ml):

        arr = random.sample(range(0,self._data.shape[0]),5)
        print(st.session_state['selected_prop'])

        if (st.session_state['selected_prop']):
            print("similar")
            p = Property(st.session_state['selected_prop'], self._data)
            # r = Recommendation(p,self._data)
            # arr = r.recommendSimilar(ml)
            arr = similarprop(st.session_state['selected_prop'], ml)
            st.header("Top property for you")
            
        else:
            print("random")
            st.header("Top property for you")
            
        # show 4 recommended property
        cols = cycle(st.columns(4))
        
        for i in range(4):
            p = Property(arr[i], self._data)
                
            type = p.property.type + "/" + str(i+1)
            # imgpath = "src/images/"+ type  + ".jpg"
            # img = Image.open(imgpath)
            with next(cols):
                # st.image(img,use_column_width =True)
                st.subheader(p.scheme() +" Property ")
                st.write('Property Type: '+ p.type())
                st.write('Bedroom Number: ' + str(p.bedroom()))
                st.write('Price: RM' + str(p.price()))
                st.button("Details",key = i, on_click = setprop, args = (arr[i],))

    def affordCheck(self):

        # view property details
        st.subheader("Affordability Checker")
        st.text("Simply fill up the following to check whether this property is worth for you")
        index = st.session_state['selected_prop']
        prop = Property(index, self._data)
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
            showEval(eval)
            # runMachineLearning(df)
            self.recommends(int(eval['max loan']))
            st.session_state['page'] = "home"