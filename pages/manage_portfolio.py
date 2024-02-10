import streamlit as st
from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os

CONFIGS = STATE()
CONFIGS.set_page_config()

UI = UI()
Auth = SB_CLIENT()

 #Landing Page
st.image(r"resources/dividend_header2.png")

show_pages([
    Page("main.py","Home",":house_with_garden:", is_section=True),
    Page(os.path.join("pages","signup.py"),"User Sign-Up",":pencil:"),
    Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:")
    ])


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
        Page(os.path.join("pages","signup.py"),"User Sign-Up",":pencil:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
        Page(os.path.join("pages","author.py"),"Author",":boy:")
        ])


pm, tx = st.tabs(["Portfolio Manager","Wallet Transactions"])
with pm:
    if st.session_state["logged-in"]:
        UI.portfolio_manager_UI()
    else:
        UI.content_unavailable()

with tx:
    if st.session_state["logged-in"]:
        UI.transaction_manager()

    else:
        UI.content_unavailable()