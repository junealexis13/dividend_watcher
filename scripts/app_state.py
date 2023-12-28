import streamlit as st
class STATE:
    def __init__(self) -> None:
        #Create a custom states. Initial States

        if 'logged-in' not in st.session_state:
            st.session_state['logged-in'] = False

        if 'viewing' not in st.session_state:
            st.session_state['viewing'] = True

        if "stock_on_view" not in st.session_state:
            st.session_state['stock_on_view'] = None
