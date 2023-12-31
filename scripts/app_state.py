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

        if "error_message" not in st.session_state:
            st.session_state["error_message"] = None

    def _dev_toggle_login_state(self):
        toggle = st.checkbox('Enable logged-in state.',value = st.session_state['logged-in'])
        if toggle:
            st.session_state['logged-in'] = True
        else:
            st.session_state['logged-in'] = False
        st.write(st.session_state['logged-in'])
