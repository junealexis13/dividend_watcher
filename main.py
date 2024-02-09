from scripts import *
from st_pages import Page, add_page_title, hide_pages, show_pages
import os


import os

if __name__ == "__main__":
    CONFIGS = STATE()
    CONFIGS.set_page_config()
    CONFIGS.__init_states()

    #Landing Page
    st.image(r"resources/dividend_header2.png")

    A = UI()
    C = DATA_PROVIDERS()
    
    Auth = SB_CLIENT()
    

    A.introduction()

    ####UI CODES AFTER HERE####


    #in sidebar
    with st.sidebar:
        A.profile_view()
        if not st.session_state["logged-in"]:
                
            show_pages([
                Page("main.py","Home",":house_with_garden:", is_section=True),
                Page(os.path.join("pages","login.py"),"Login",":pencil:"),
                Page(os.path.join("pages","signup.py"),"User Sign-Up",":key:"),
                Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
                Page(os.path.join("pages","author.py"),"Author",":boy:"),

                ])
            
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
            
    wallet, dividend_screener, current_equity, viewer = st.tabs(["Wallet","Screener", "Equity", "Viewer"])
    
    with wallet:
        A.wallet_manager()

    with dividend_screener:
        A.section_body1()

    with current_equity:
        A.section_body2()

    with viewer:
        A.section_body3()
        

    with st.expander("debug message"):
        st.write(st.session_state['error_message'])