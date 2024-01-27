import streamlit as st
import os
from st_pages import Page, show_pages, hide_pages

show_pages([
        Page("main.py","Home",":house_with_garden:"),
        Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
        Page(os.path.join("pages","author.py"),"Author",":boy:")
        ])
st.image(r"resources/dividend_header2.png")

show_pages([
        Page("main.py","Home",":house_with_garden:"),
        Page(os.path.join("pages","login.py"),"User Sign-Up",":pencil:"),
        Page(os.path.join("pages","manage_portfolio.py"),"Manage Portfolio",":money_mouth_face:"),
        Page(os.path.join("pages","author.py"),"Author",":boy:")
        ])


with st.sidebar:
    if st.session_state["logged-in"]:
        hide_pages(["User Sign-Up"])
        
st.markdown(
    '''
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
<style> .center_title {text-align: center; font-family: Roboto;} </style>
<style> .header_2 {text-align: center; font-family: Roboto;} </style>
<style> .title_styling {font-size: 3rem;  font-weight: 500;} </style>
<style> .header_styling {font-size: 2rem;  font-weight: 500;} </style>
<style> .subheader_styling {font-size: 1.25rem;  font-weight: 500;} </style>
<style> .caption_styling {font-size: 0.85rem;color: white;} </style>
<style> .script_styling {font-size: 1rem;color: white;text-align:justify;} </style>
</head>
    '''
,
    unsafe_allow_html=True
)

st.markdown("<p class='center_title title_styling'>About the author</p>", unsafe_allow_html=True)
st.divider()

with st.container(border=False):
    _, mid, _ = st.columns([1,1,1])
    with mid:
        st.image(os.path.join("resources","dp.png")) 
    st.markdown('''<p class="center_title header_styling" >Hi guys👋! I am <b>June Alexis</b></p>''', unsafe_allow_html=True)
    st.markdown("<p class='center_title caption_styling'>Just a nobody creating something for anybody.</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown('''<p class='script_styling'>So, picture this: back in 2020, I'm hit with this genius idea to dive into molecular dynamics simulation🧬 like, really? Am I out of my mind?😰 That's for my master's thesis tho.<br><br>By the way, let me drop a little science on you - I'm a chemist by day, mixing potions and all that. But truth be told, the lab life was getting kinda stale. That's why I'm venturing into the wild world of programming. It's like, "Lab, you had your time, but I need something more, you know?" Anyway, back to the story.<br><br> My cool adviser (he's super cool yes 😎🆒) convinces me it's a good move, and against all odds, I roll with it.Now, here's the kicker – <b>I don't know jack about programming</b>. Zero 0️⃣ , nada 🤷‍♀️. But ye boy's determined. I ain't backing down. So, I wrestle with Python 🐍, swear I won't leave this adventure without some coding skills, and wouldn't you know it, I end up falling in love 😍🥰 with it.
<br><br>Fast forward through a monthly bootcamp subscription, lots of coffee (big up, CAFFEINE!☕☕☕), and a sprinkle of that GENERATIVE AI magic 🤖✨ and bam! Here I am, cooking up both goofy and hopefully kinda useful stuff. It's a wild ride, and I'm living for it. LOL.
<br><br>Shoutout to all you awesome folks for riding this wave with me and supporting my app. I hope it brings a smile to your face or even solves a little problem. Your support means the world, for real. Here's to keeping it real and having a blast y'all stay cool! Cheers!🍻🍻🍻</p>''', unsafe_allow_html=True)
    st.divider()
    st.markdown('''<p class="subheader_styling" >In case you want to reach out, here's my socials.</b></p>''', unsafe_allow_html=True)
    with st.container():
        st.write("X (twitter): @juniekemz")
        st.write("GitHub: junealexis13")