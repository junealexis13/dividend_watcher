from scripts import *
import os

if __name__ == "__main__":

    #Landing Page
    st.image(os.path.join(os.getcwd(),"resources", "dividend_header2.png"))

    A = UI()
    B = STATE()
    A.introduction()

    #in sidebar
    with st.sidebar:
        A.profile_view()
        B._dev_toggle_login_state()

        with st.expander("debug message"):
            st.write(st.session_state['error_message'])
    
    dividend_screener, current_equity = st.tabs(["Screener", "Equity"])
    
    with dividend_screener:
        A.section_body1()

    with current_equity:
        A.section_body2()