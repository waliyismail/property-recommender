import math
import numpy_financial as npf
import streamlit as st

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
        maxloan = math.ceil(instalment * 200)
        reqloan = math.ceil(self._price * 0.9)
        mindp = math.ceil(self._price - maxloan if (self._price > maxloan) else self._downpayment)
        interestRate = self._interest/100 # in decimal
        period = self._loanterm * 12 # in months
        eligibleInst = math.ceil(npf.pmt(interestRate/12, period, maxloan) * -1)
        reqInst = math.ceil(npf.pmt(interestRate/12, period, reqloan) * -1)
        eligibility = True if (self._price < maxloan) else False
        return {"net income": str(net_income), "commitment": str(commitment), "max loan": str(maxloan), 
                    "required loan": str(reqloan),"required installment": str(reqInst), "eligible installment": str(eligibleInst), 
                    "min downpayment": str(mindp), "eligibility": eligibility }

    def showEval(self, eval):
        st.success("Evaluation Report successfully created" )
        st.subheader("Affordability Evaluation Report")

        with st.container():
            st.text_input("Monthly Net Income: ", "RM" + eval['net income'], disabled=True)
            st.text_input("Monthly Commitment: ", "RM" + eval['commitment'], disabled=True)
            c1,c2= st.columns(2)
            c1.text_input("Loan Required: ", "RM" + eval["required loan"], disabled=True)
            c2.text_input("Max Eligible Loan: ", "RM" + eval["max loan"], disabled=True)
            c1,c2= st.columns(2)
            c1.text_input("Monthly Installment Required: ", "RM" + eval["required installment"], disabled=True)
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
            st.header("Consider these property below")
            # set affordable property page
            
