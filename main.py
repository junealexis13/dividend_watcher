from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os


import os

if __name__ == "__main__":
    CONFIGS = STATE()
    CONFIGS.set_page_config()


    #Landing Page
    st.image(r"resources/dividend_header2.png")

    A = UI()
    C = DATA_PROVIDERS()
    
    Auth = SB_CLIENT()
    

    A.introduction()

    show_pages([
        Page("main.py","Home",":house_with_garden:", is_section=True),
        Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:")
        ])



    ####UI CODES AFTER HERE####


    #in sidebar
    with st.sidebar:
        A.profile_view()
        if not st.session_state["logged-in"]:
                
            show_pages([
                Page("main.py","Home",":house_with_garden:", is_section=True),
                Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
                Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
                Page(os.path.join("pages","author.py"),"Author",":boy:")
                ])
            with st.form("user-login-main"):
                user_login,user_pass = A.login_ui()

                login = st.form_submit_button(label="Sign in")
                if login:
                    try:
                        if (user_login, user_pass) == (st.secrets['admin']['USER'],st.secrets['admin']['PASSWORD']):
                            st.session_state['logged-in'] = True
                            st.session_state['is_admin'] = True
                            st.rerun()
                        else:
                            Auth.signIn_User(user_login,user_pass)
                            Auth.fetch_user_info()
                            st.rerun()
                    except Exception as e:
                        st.error(e)
                    
                
        elif st.session_state["logged-in"]:
            show_pages([
                Page("main.py","Home",":house_with_garden:", is_section=True),
                Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
                Page(os.path.join("pages","author.py"),"Author",":boy:")
                ])
            

            logout = st.button("Log out",key="logout-button")
            if logout:
                Auth.signOut()

            st.divider()
            if st.session_state['active_stockPicks'] is not None:
                Auth.create_selection()
                st.write(st.session_state["active_stockPicks"])
            else:
                st.write("No Stockpicks Detected. Consider creating one.")
                create_sp = st.button("Create now")
                if create_sp:
                    st.switch_page(os.path.join("pages","manage_portfolio.py"))
            
    dividend_screener, current_equity, __prototype_view = st.tabs(["Screener", "Equity", "Viewer"])
    
    with dividend_screener:
        A.section_body1()

    with current_equity:
        A.section_body2()

    with __prototype_view:
        A.section_body3()
        

    with st.expander("debug message"):
        st.write(st.session_state['error_message'])