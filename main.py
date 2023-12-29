from scripts import *

if __name__ == "__main__":

    #Landing Page
    st.image("resources/dividend_header2.png")

    A = UI()
    A.introduction()

    #in sidebar
    with st.sidebar:
        A.profile_view()
    
    dividend_screener, current_equity = st.tabs(["Screener", "Equity"])
    
    with dividend_screener:
        A.section_body1()

    with current_equity:
        st.write("Equity Stats will show here... but not now.")