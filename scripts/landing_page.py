import streamlit as st
from datetime import datetime
from scripts.configs import TOML
from scripts.data_parser import StockData
from scripts.app_state import STATE
from scripts.exceptions import *

class UI:
    def __init__(self) -> None:
        #instantiate configs
        self.TOML = TOML()
        self.DATA = StockData()
        self.SessionStates = STATE()
        self.cols = self.TOML.get_stockpicks()
        self.current_datetime = datetime.now()

    def create_columns(self, ticker_name):
        #create cols
        col_nums = 3
        cols = st.columns(col_nums)

        #iterate through cols created
        try:
            #Fetch the info in PD Form
            curr, prev = self.DATA.pack_dividend_data(ticker_name)
            delta_value = curr - prev
            with cols[0]:
                st.metric(f"DV YLD ({str(self.current_datetime.year)}) ",f"₱{round(curr,2)}/s", delta = round(delta_value, 2))
                st.markdown(f"<p style ='font-size:0.75rem;'>₱ {round(prev,2)}/s ({str(self.current_datetime.year-1)})</p>", unsafe_allow_html=True)

        except Dividend_Data_Error:
            st.error("Recently added stocks does not have a Dividend Data. Consider other dividend stocks.")

        except AttributeError:
            if ticker_name is None:
                st.info('Choose dividend stock to view.')
            else:
                st.error('Problem with Data Parser')
        

    
    def introduction(self):
        st.caption('''<!DOCTYPE html>
<html>
<head>
<style> p {text-align: justify;} </style>
<style> p {font-family: Monospace} </style>
<style> b {color: white;} </style>
</head>
<body>

<p>
Welcome to the Dividend Screener app, your go-to platform for tracking and analyzing dividends listed on the <b>Philippine Stock Exchange</b>. Our app is designed to help you make informed investment decisions by providing real-time data, comprehensive screening tools, and in-depth analysis of companies offering dividends. Whether you’re a seasoned investor or just starting out, the Dividend Screener app is an essential tool for anyone looking to invest in dividend stocks in the Philippines. Start your journey towards smarter investing today with the Dividend Screener app!
</p>

</body>
</html>''', unsafe_allow_html=True)
        
    def profile_view(self):
        with st.container(border=True):
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                st.image('resources/user.png', use_column_width = True)

            with col2:
                if not st.session_state['logged-in']:
                    st.markdown('<p style="font-size:2rem; font-family:Fantasy;">Logged in as: <span style="color:#ffde59; font-size:2.2rem; font-family:Fantasy;">GUEST</span></p>', unsafe_allow_html=True)
                    st.caption("Login or register an account.")
                else:
                    st.header("*VIEWING THE PROFILE IF LOGGED IN*")

    def custom_selection(self):
        if not st.session_state["logged-in"]:
            stockPick = st.selectbox(
                    'View Dividend Stock',
                    self.TOML.get_PSE_list(),
                    index=None,
                    help='Choose what Stock Dividends to show')
            return stockPick
        
        else:
            options = st.multiselect(
                    'View Annual Dividend Data',
                    self.TOML.get_PSE_list(),
                    self.TOML.get_stockpicks(), max_selections= 5,
                    help='Choose what Stock Dividends to show')
            return options
        
    def section_body1(self):
        if not st.session_state["logged-in"]:
            try:
                stocks = self.custom_selection()            
                with st.container(border=True):
                    st.markdown(f'''<p style="font-size: 2rem; text-align: center; font-family: Fantasy;"> {stocks} - {self.TOML.get_company_name(stocks)[0]}</p>''', unsafe_allow_html=True)
                    self.create_columns(stocks)
            except TypeError as e:
                st.error(f'Error message. {e}')