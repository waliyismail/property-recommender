from ml import runMachineLearning
import streamlit as st
import pandas as pd
from persist import load_widget_state
from frontend import App, showEval

data= pd.read_csv('src/data/kl_cleaned_v2.csv')
app = App(data)
def main():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update(app.setStates())

    page = "home"
    PAGES[page]()
    page = st.session_state['page']
    print(page)
    if( page == 'propdetails'):
        print(1)
        PAGES["propdetails"]()
        PAGES["recommend"](-1)
    elif(page == 'affordability'):
        print(2)
        PAGES['affordability']()
    else:
        print(3)
        PAGES["filter"]()
        PAGES["recommend"](-1)
    print("=====one loop====")

PAGES = {
    "home": app.home,
    "filter": app.filters,
    "recommend": app.recommends,
    "propdetails": app.details,
    "affordability": app.affordCheck,
}


if __name__ == "__main__":
    load_widget_state()
    main()
