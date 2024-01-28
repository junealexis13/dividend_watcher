import streamlit as st
from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os

CONFIGS = STATE()
CONFIGS.set_page_config()

UI = UI()
MNGR = PORTFOLIO_MANAGER()
Auth = SB_CLIENT()

 #Landing Page
st.image(r"resources/dividend_header2.png")


with st.sidebar:
    if st.session_state["logged-in"]:
        show_pages([
        Page("main.py","Home",":house_with_garden:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
        Page(os.path.join("pages","author.py"),"Author",":boy:")
        ])


    else:
        show_pages([
        Page("main.py","Home",":house_with_garden:"),
        Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
        Page(os.path.join("pages","author.py"),"Author",":boy:")
        ])

        user_login,user_pass = UI.login_ui()

        login = st.button("Sign in",key="login-button")
        if login:
            try:
                Auth.signIn_User(user_login,user_pass)
                st.rerun()
            except Exception as e:
                st.error(e)

if st.session_state["logged-in"]:
    UI.portfolio_manager_UI()
else:
    st.divider()
    UI.content_unavailable()