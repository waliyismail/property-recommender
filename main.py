import streamlit as st
import pandas as pd
from persist import load_widget_state
from frontend import App

data= pd.read_csv('src/data/kl_cleaned_v2.csv')
app = App(data)
def main():
    if "page" not in st.session_state:
        # Initialize session state.
        st.session_state.update(app.setStates())

    page = "home"
    PAGES[page]()
    if(st.session_state['rec']):
        PAGES["recommend"]()
    elif(st.session_state['eval']):
        PAGES['affordability']()
    else:
        PAGES["filter"]()
        PAGES["recommend"]()


PAGES = {
    "home": app.home,
    "filter": app.filters,
    "recommend": app.recommends,
    "affordability": app.affordCheck,
}


if __name__ == "__main__":
    load_widget_state()
    main()
