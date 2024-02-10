import streamlit as st
import os

class STATE:
    def __init__(self) -> None:
        #Create a custom states. Initial States
        pass

    def init_states(self):
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

        if "user_metadata" not in st.session_state:
            st.session_state["user_metadata"] = None

        if "active_stockPicks" not in st.session_state:
            st.session_state["active_stockPicks"] = None

        if "user_wallet" not in st.session_state:
            st.session_state["user_wallet"] = None

        if "active_wallet" not in st.session_state:
            st.session_state["active_wallet"] = None

        if "user_transactions" not in st.session_state:
            st.session_state["user_transactions"] = None

        if 'wallet_stat' not in st.session_state:
            st.session_state['wallet_stat'] = None

    def set_page_config(self):
        st.set_page_config(layout='centered',page_title='PSE-Div Screener',page_icon=os.path.join("resources","page_icon.ico"))
