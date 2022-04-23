import streamlit as st
import pickle
import pandas as pd
import random
from PIL import Image
import string
from persist import persist, load_widget_state
from functions import *
###### IMPORT DATA #######
rawData= pd.read_csv('../../data/kl_cleaned_v2.csv')
minPrice = rawData['price'].min().item()
maxPrice = rawData['price'].max().item()

kldf = pickle.load(open('../property_list.pkl','rb'))
similarity = pickle.load(open('../similarity.pkl','rb'))

propertylist = rawData['address'].values
schemelist = rawData['scheme'].unique()
roomlist = rawData['bedroom-num'].unique()
typelist = rawData['property-type'].unique()
##########################################




############### PAGES ####################
def main():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update({
            # Default page.
            "page": "home",
            # Data used
            "data": rawData,
            # Filter options.
            "states": ['Kuala Lumpur','Selangor'],
            "schemelist": schemelist,
            "typelist": typelist,
            "roomlist": roomlist,
            "prioritylist": ['state','scheme', 'price', 'property type', 'housing size'],

            # Default filter values.
            
            "rec": False,
            "eval": False,
            "clicked": 0,
            "sel_prop": 0,
        })
    
    #page = st.sidebar.radio("Select your page", tuple(PAGES.keys()), format_func=str.capitalize)
    page = "home"
    PAGES[page]()
    if(st.session_state['rec']):
        PAGES["rec_page"]()
    elif(st.session_state['eval']):
        PAGES['eval']()
    else:
        PAGES["filter"]()
        PAGES["rec_page"]()
    
    
def home():
    st.title("Property Recommender")
    st.text("A Property Recommender Website Using Machine Learning")


# Filters property UI a
def filters():
    st.subheader("Filter your desire")
    filter_expander = st.expander("Property Filter")
    with filter_expander:
        filter_form = st.form(key='filter')
        c1,c2= filter_form.columns([1,2])
        c1.selectbox('State', st.session_state['states'])
        c2.multiselect('Project Scheme e.g (Taman, Desa, etc )', st.session_state['schemelist'], key = persist("scheme"))
        filter_form.multiselect('Property Type', st.session_state['typelist'], key = persist("type"))
        filter_form.multiselect('Room Number', st.session_state['roomlist'], key = persist("room"))
        c1,c2 = filter_form.columns(2)
        c1.number_input("Minimum Price (RM)", minPrice, key=persist("minprice"))
        c2.number_input("Maximum Price (RM)", maxPrice, key=persist("maxprice"))
        
        # filter_form.multiselect('Choose your desired priority (High to Low)', st.session_state['prioritylist'], key = persist("priority")) # get priority choosen by user
        submit_button = filter_form.form_submit_button("Recommends Me Property!")
    if submit_button:
        applyFilter()
        st.success("Filter Applied")


from itertools import cycle

filteredImages = [] # your images here
caption = [] # your caption here
cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=150, caption=caption[idx])

def recommends():

    if st.session_state['rec']:
        # arr= [0,1,2,3,4]
        st.session_state['rec'] = False
        # st.success(st.session_state['sel_prop'])
        with st.container():
            index = 1
            randpic = random.randint(1,3)
            ptype = getProperty().type +"/" + str(randpic)
            imgpath = "src/images/semid/2.jpg"
            img = Image.open(imgpath)
            st.image(img, width =500)
            st.markdown("### " + string.capwords(rawData.iloc[index]['scheme']) + " Property")
            st.markdown ('##### Price: RM' + str(rawData.iloc[index]['price']))
            st.text('Petaling, Kuala Lumpur' )
            c1, c2 = st.columns(2)
            c1.write('Property Type: ' + str(rawData.iloc[index]['property-type']))
            c2.write('Tenure Type: ' + rawData.iloc[index]['tenure-type'])
            c1, c2 = st.columns(2)
            c1.write('Building Size (sqm): 354' )
            c2.write('Bedroom Number: ' + str(rawData.iloc[index]['bedroom-num']))
            
            st.button("Evaluate Affordability", on_click=setEval, help= "Check your affordability for this property" )
    
        st.header("Top similar property")
        arr = similarprop(index)
    else:
        st.header("Top Property For You")
        arr = random.sample(range(0,rawData.shape[0]),5)



# filteredImages = [] # your images here
# caption = [] # your caption here
# cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
# for idx, filteredImage in enumerate(filteredImages):
#     next(cols).image(filteredImage, width=150, caption=caption[idx])
    # cols = st.columns(4)
    cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
    for i in range(4):
        
        #   if property type == blah,  open image blah-#Num rand 1-5
        # type = rawData.iloc[arr[i]].type
        ptype = rawData.iloc[arr[i]].type + "/"
        imgpath = "src/images/terrace/" + str(i+1) + ".jpg"
        img = Image.open(imgpath)
    
        with next(cols):
            st.image(img,use_column_width =True)
            st.subheader(rawData.iloc[arr[i]].scheme +" Property ")
            st.write('Property Type: '+ rawData.iloc[arr[i]]['property-type'])
            st.write('Bedroom Number: ' + str(rawData.iloc[arr[i]]['bedroom-num']))
            st.write('Price: RM' + str(rawData.iloc[arr[i]]['price']))
            st.button("Details",key = i, on_click = setprop, args = (arr[i],))

        # ptype = rawData.iloc[arr[i]].type + "/"
        # imgpath = "src/images/" + ptype + str(1) + ".jpg"
        # img = Image.open(imgpath)
        # x.subheader(rawData.iloc[arr[i]].scheme +" Property ")
        # x.image(img)
        # x.write('Property Type: '+ rawData.iloc[arr[i]]['property-type'])
        # x.write('Bedroom Number: ' + str(rawData.iloc[arr[i]]['bedroom-num']))
        # x.write('Price: RM' + str(rawData.iloc[arr[i]]['price']))
        # x.button("Details",key = i, on_click = setprop, args = (arr[i],))


    

def evalAfford():

    #st.success(st.session_state['sel_prop'])
    # view property details
    st.subheader("Affordability Checker")
    st.text("Simply fill up the following to check whether this property is worth for you")
    
    prop = getProperty()
    
    fr = st.form("eval-form")
    with fr:
        st.text_input("Property: ",prop.scheme , disabled=True)
        st.text_input("Property Price (RM)",prop.price, disabled=True)
        st.number_input("Downpayment (RM) (10%)", (10*prop.price)/100, key=persist("downpayment"))
        with st.container():
            st.text("Earnings and Commitment Section")
            st.number_input("Monthly Gross Salary (RM)",  key=persist("salary"))
            st.number_input("Monthly PCB (RM)",  key=persist("pcb"))
            st.number_input("Current Loan (RM) (Cars, Home, PTPTN, etc) ",  key=persist("loan"))
        with st.container():
            st.text("Mortgage Details Section")
            st.number_input("Loan Term (Years)",min_value = 10, key=persist("loanterm"))
            st.slider("Interest Rate (%)", 0.0, 10.0, 3.5,  key=persist("interest"))
    if fr.form_submit_button("Evaluate!"):
        showEval()
        st.session_state['eval'] = False
        

PAGES = {
    "home": home,
    "filter": filters,
    "rec_page": recommends,
    "eval": evalAfford,
}


if __name__ == "__main__":
    load_widget_state()
    main()