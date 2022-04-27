from ml import runMachineLearning
import streamlit as st
import pandas as pd
from persist import load_widget_state
from frontend import App
st.set_page_config(page_title="Property Recommender")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

data= pd.read_csv('src/data/kl_cleaned_v2.csv')
app = App(data)
#runMachineLearning(data)
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
        PAGES["recommend"](st.session_state['affordable'])
    elif(page == 'affordability'):
        print(2)
        PAGES['affordability']()
        # PAGES["recommend"](st.session_state['affordable'])
    else:
        print(3)
        PAGES["filter"]()
        PAGES["recommend"](st.session_state['affordable'])
    print("=====one loop====")

    # st.button("home", on_click =st.session_state.update(app.setStates()) )
        
        # st.session_state['page'] = "home"


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
