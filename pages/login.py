import streamlit as st
from scripts import *

__login = SB_CLIENT()
__add_tools = ADDRESS_TOOLS()


##Set Styling
st.markdown(
    '''
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
<style> .center_title {text-align: center; font-family: Roboto;} </style>
<style> .header_2 {text-align: center; font-family: Roboto;} </style>
<style> .title_styling {font-size: 3rem;  font-weight: 500;} </style>
<style> .subheader_styling {font-size: 1.25rem;  font-weight: 500;} </style>
<style> .caption_styling {font-size: 0.75rem;color: #9E9E9E;} </style>
</head>
    '''
,
    unsafe_allow_html=True
)


st.markdown("<p class='center_title title_styling'>New User Sign-Up</p>", unsafe_allow_html=True)
st.markdown("<p class='center_title caption_styling'>Create an account for free.</p>", unsafe_allow_html=True)
st.divider()


st.markdown("<p class='center_title subheader_styling'>Login Credentials</p>", unsafe_allow_html=True)
signUp_email = st.text_input("email",max_chars=50)
signUp_pass = st.text_input("password",type="password", max_chars=30)
st.divider()
with st.container(border=True):
    st.markdown("<p class='center_title subheader_styling'>Personal Information</p>", unsafe_allow_html=True)
    signUp_Fname = st.text_input("First name",max_chars=50)
    signUp_Lname = st.text_input("Last name",type="default", max_chars=30)

with st.container(border=True):
    st.markdown("<p class='center_title subheader_styling'>Address</p>", unsafe_allow_html=True)
    
    signUp_region = st.selectbox("Region",__add_tools.get_regions())

    if signUp_region is not None:
        signUp_province = st.selectbox("Province",__add_tools.get_province(signUp_region))

    if signUp_region is not None or signUp_province is not None:
        signUp_city_muni = st.selectbox("City/Municipality",__add_tools.get_city_muni(signUp_province))

    if signUp_region is not None or signUp_province is not None or signUp_city_muni is not None:
        signUp_brgy = st.selectbox("Barangay/Village",__add_tools.get_brgy(signUp_city_muni))

signUp_bday = st.date_input("Your birthday :balloon:")
signUp_gender = st.selectbox("Gender",["Male","Female","Prefer not to say","None of the above"])
submit = st.button("Submit and Create Account")
if submit:
    __info_mgr = USER_INFO_MNGR(
        signUp_Fname,
        signUp_Lname,
        signUp_region,
        signUp_province,
        signUp_city_muni,
        signUp_brgy,
        signUp_bday,
        signUp_gender)
    try:
        __login.register_User(signUp_email, signUp_pass, __info_mgr.pack_data())
        st.info(f"Confirmation link has been sent to {signUp_email}")
    except Exception as e:
        st.warning("An error occured.")
        print(e)
st.divider()
st.markdown("<p class='center_title caption_styling'>All information you provided here will be encrypted. I promise.</p>", unsafe_allow_html=True)