from scripts import *

if __name__ == "__main__":

    #Landing Page
    st.image("resources/dividend_header2.png")

    A = UI()
    A.introduction()

    #in sidebar
    with st.sidebar:
        A.profile_view()
    
    A.section_body1()