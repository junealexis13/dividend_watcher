import streamlit as st
import os
class STATE:
    def __init__(self) -> None:
        #Create a custom states. Initial States

        if 'logged-in' not in st.session_state:
            st.session_state['logged-in'] = False

        if 'viewing' not in st.session_state:
            st.session_state['viewing'] = True

        if "stock_on_view" not in st.session_state:
            st.session_state['stock_on_view'] = None

        if "error_message" not in st.session_state:
            st.session_state["error_message"] = None

        if "is_admin" not in st.session_state:
            st.session_state["is_admin"] = False

        if "logged-in_user" not in st.session_state:
            st.session_state["logged-in_user"] = None

        if "user_metadata" not in st.session_state:
            st.session_state["user_metadata"] = None

    def _dev_toggle_login_state(self):
        toggle = st.checkbox('Enable logged-in state.',value = st.session_state['logged-in'])
        if toggle:
            st.session_state['logged-in'] = True
        else:
            st.session_state['logged-in'] = False
        st.write(st.session_state['logged-in'])


    def set_page_config(self):
        st.set_page_config(layout='centered',page_title='PSE-Div Screener',page_icon=os.path.join("resources","page_icon.ico"))
