
import streamlit as st
import pickle
import pandas as pd
import numpy_financial as npf
import random
from PIL import Image
import string
import math
kldf = pickle.load(open('../property_list.pkl','rb'))
similarity = pickle.load(open('../similarity.pkl','rb'))
rawData= pd.read_csv('../../data/kl_cleaned_v2.csv')
############### FUNCTIONS ################
#Filter functions 
def applyFilter():

    #priority, scheme, type, room number, price
    df = st.session_state['data']
    if st.session_state['scheme']:
    #filter scheme
        for i in st.session_state['scheme']:
            df = df[df['scheme'] == i]

    if st.session_state['type']:
        for i in st.session_state['type']:
            df = df[df['property-type'] == i]
    
    if st.session_state['room']:
        for i in st.session_state['room']:
            df = df[df['bedroom-num'] == i]


    df = df[(df['price'] >= (st.session_state['minprice']) ) & (df['price'] <= (st.session_state['maxprice']))]

    st.session_state['data'] = df

def setprop(x):
    st.session_state['sel_prop'] = x
    st.session_state['rec'] = True

def setEval():
    st.session_state['eval'] = True

def displayProp(option):
    #display property 

    # if option == 'top 5':
    #     #display 5 property
    # elif option == "selected":
    #     #display 1 property
    # elif option == 'similar prop':
        #display

    pass

def getProperty():
    index = st.session_state['sel_prop']
    return rawData.iloc[index]
     
def recommendAffordable():
    pass

"""Do the required calculation for property evaluations'

Returns
--------
    dictionary of evaluation values
"""
def evalAffordability():
    propertyPrice = getProperty().price
    net_income = st.session_state['salary'] - st.session_state['pcb']
    commitment = st.session_state['loan']
    maxdebt = 0.7 * net_income
    instalment = maxdebt - commitment
    maxloan = instalment * 200
    mindp = propertyPrice - maxloan
    interestRate = st.session_state['interest']/100 # in decimal
    period = st.session_state['loanterm'] * 12 # in months
    eligibleIns = math.ceil(npf.pmt(interestRate/12, period, maxloan) * -1)

    return {"net income": net_income, "commitment": commitment, "max loan": maxloan,
                "eligible installment": eligibleIns, "minimum downpayment": mindp }

def showEval():
    st.success("Evaluation Report successfully created" )
    st.subheader("Affordability Evaluation Report")
    propertyPrice = getProperty().price
    net_income = st.session_state['salary'] - st.session_state['pcb']
    commitment = st.session_state['loan']
    maxdebt = 0.7 * net_income
    instalment = maxdebt - commitment
    maxloan = instalment * 200
    mindp = propertyPrice - maxloan # if -ve, same dengan 10percent
    interestRate = 3.5/100 # in decimal
    period = 35 * 12 # in months
    eligibleMortgage = math.ceil(npf.pmt(interestRate/12, period, 378000) * -1)



    with st.container():
        st.write("Monthly Net Income: RM 3200")
        st.write("Monthly Commitment: RM 450 " )
        st.write("Max Eligible Loan: RM 378000")
        st.write("Monthly Installment: RM " + str(eligibleMortgage))
        st.write("Minimum Downpayment Required: RM 20000")
    
    with st.container():
        st.subheader("Overall Recommendations")
        st.text("This property is affordable by you")
        st.text("You can still own a higher value property up to your max loan amount (RM 378000)")
        
    with st.container():
        # find property below max loan
        st.text("these are the property affordable for you")
        # recommendAffordable()
    
    st.button("Back Home")

# def showEval():
#     st.success("Evaluation Report successfully created" )
#     st.subheader("Affordability Evaluation Report")
#     propertyPrice = getProperty().price
#     net_income = st.session_state['salary'] - st.session_state['pcb']
#     commitment = st.session_state['loan']
#     maxdebt = 0.7 * net_income
#     instalment = maxdebt - commitment
#     maxloan = instalment * 200
#     mindp = propertyPrice - maxloan
#     interestRate = st.session_state['interest']/100 # in decimal
#     period = st.session_state['loanterm'] * 12 # in months
#     eligibleMortgage = math.ceil(npf.pmt(interestRate/12, period, maxloan) * -1)



#     with st.container():
#         st.write("Monthly Net Income: RM " + str(net_income))
#         st.write("Monthly Commitment: RM" + str(commitment))
#         st.write("Max Eligible Loan: RM" + str(maxloan))
#         st.write("Monthly Installment: RM" + str(eligibleMortgage))
#         st.write("Minimum Downpayment Required: RM" + str(mindp))
    
#     with st.container():
#         st.subheader("Overall Recommendations")
#         if( maxloan < propertyPrice*0.9 ):

#             st.text("1. You need to prepare downpayment required ")
#             st.text("2. Find cheaper property ")
#         else:
#             st.text("This property is affordable by you")
        
#     with st.container():
#         # find property below max loan
#         st.text("these are the property affordable for you")
#         # recommendAffordable()
    
#     st.button("Back Home")

"""find similar property from cosine similarity
Parameters
---------
    index : int, required
        The index value of selected property 
Returns
--------
    list of indices of similar property
"""
def similarprop(index):
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    distances = distances[1:6]
    arr = [i[0] for i in distances]
    return arr