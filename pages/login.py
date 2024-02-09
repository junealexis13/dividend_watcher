from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os

st.set_page_config(layout='centered',page_title='PSE-Div Screener',page_icon=os.path.join("resources","page_icon.ico"))

st.image(r"resources/dividend_header2.png")
UI = UI()
Auth = SB_CLIENT()
st.divider()


st.markdown(f"<h1 style='text-align: center;padding-top: 0;'>Welcome to PH Dividend Watcher!</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;padding-top: 0;'>Please login to use the app.</p>", unsafe_allow_html=True)


show_pages([
    Page("main.py","Home",":house_with_garden:", is_section=True),
    Page(os.path.join("pages","login.py"),"Login",":pencil:"),
    Page(os.path.join("pages","signup.py"),"User Sign-Up",":key:"),
    Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
    Page(os.path.join("pages","author.py"),"Author",":boy:"),

    ])


with st.form("user-login-main"):
    user_login,user_pass = UI.login_ui()

    login = st.form_submit_button(label="Sign in")
    if login:
        try:
            Auth.signIn_User(user_login,user_pass)
            st.switch_page("main.py")
        except Exception as e:
            st.error(e)