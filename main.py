from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os


import os

if __name__ == "__main__":

    #Landing Page
    st.image(r"resources/dividend_header2.png")

    A = UI()
    B = STATE()
    Auth = SB_CLIENT()
    A.introduction()

    show_pages([
        Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
        Page("main.py","Home",":home:")
    ])

    ####UI CODES AFTER HERE####


    #in sidebar
    with st.sidebar:
        A.profile_view()

        if not st.session_state["logged-in"]:

                user_login,user_pass = A.login_ui()

                login = st.button("Sign in",key="login-button")
                if login:
                    try:
                        Auth.signIn_User(user_login,user_pass)
                        st.rerun()
                    except Exception as e:
                        st.error(e)
                    
                
        elif st.session_state["logged-in"]:
            hide_pages(["User Sign-up"])
            logout = st.button("Log out",key="logout-button")
            if logout:
                Auth.signOut()
                        

    dividend_screener, current_equity = st.tabs(["Screener", "Equity"])
    
    with dividend_screener:
        A.section_body1()

    with current_equity:
        A.section_body2()

    with st.expander("debug message"):
        st.write(st.session_state['error_message'])