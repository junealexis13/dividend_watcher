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

    def create_columns(self, stock_picks = []):
        if not st.session_state["logged-in"]:
            #create cols
            col_nums = 5
            cols = st.columns(col_nums)

            #iterate through cols created
            try:
                for col_name, col in zip(stock_picks, cols):
                    #Fetch the info in PD Form

                    df = self.DATA.pack_dividend_data(col_name)

                    current_div_data = df.loc[(df["Year"] == str(self.current_datetime.year)) & (df["Type"] == "Cash")]
                    current_total_div = sum([float(x.strip("Php")) for x in current_div_data["Rate"]])

                    prev_div_data = df.loc[(df["Year"] == str(self.current_datetime.year - 1)) & (df["Type"] == "Cash")]
                    prev_total_div = sum([float(x.strip("Php")) for x in prev_div_data["Rate"]])

                    with col:
                        col.metric(col_name,f"₱{round(current_total_div,2)}",f"₱ {round(prev_total_div,2)}" )

                    #Reset the current_div_data each loop to address the problem


            except Dividend_Data_Error:
                st.error("Recently added stocks does not have a Dividend Data. Consider other dividend stocks.")
            
        else:
            #create cols
            col_nums = len(self.cols)
            cols = st.columns(col_nums)

            #iterate through cols created
            for col_name, col in zip(self.cols, cols):
                with col:
                    st.header(col_name)
    
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
                    st.markdown('<p style="font-size:2rem; font-family:Fantasy;">Logged in as: <span style="color:#ffde59; font-size:2.5rem; font-family:Fantasy;">GUEST</span></p>', unsafe_allow_html=True)
                    st.caption("Login or register an account.")
                else:
                    st.header("*VIEWING THE PROFILE IF LOGGED IN*")

    def custom_selection(self):
        if not st.session_state["logged-in"]:
            options = st.multiselect(
                    'View Stock Picks',
                    self.TOML.get_PSE_list(),
                    [], max_selections= 5,
                    help='Choose what Stock Dividends to show')
            return options
        
        else:
            options = st.multiselect(
                    'View Annual Dividend Data',
                    self.TOML.get_PSE_list(),
                    self.TOML.get_stockpicks(), max_selections= 5,
                    help='Choose what Stock Dividends to show')
            return options
        
    def section_body1(self):
        if not st.session_state["logged-in"]:
            with st.expander("Show quick dividend details"):
                st.divider()
                stocks = self.custom_selection()
                self.create_columns(stocks)