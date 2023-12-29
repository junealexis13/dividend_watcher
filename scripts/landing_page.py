import streamlit as st
import pandas as pd
import threading
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
        
    def load_equity_data(self):
        self.PSE_stats = self.DATA.get_stock_stats(st.session_state['stock_on_view']) 
        data_stock = self.PSE_stats['stock'][0]
        st.metric("Current Equity Data",f"₱{data_stock['price']['amount']}",f"{data_stock['percent_change']}%")
        st.markdown(f"<p style ='font-size:0.75rem;'>Latest Vol. {int(data_stock['volume']):,}</p>", unsafe_allow_html=True)

    def create_columns(self, ticker_name):
        #create cols
        col_nums = 3
        cols = st.columns(col_nums)

        #iterate through cols created
        try:
            #Fetch the info in PD Form
            curr, prev, curr_price, prev_percent = self.DATA.pack_dividend_data(ticker_name)
            delta_value = curr - prev
            with cols[0]:
                st.metric(f"DV YLD ({str(self.current_datetime.year)}) ",f"₱{round(curr,2)}/s", delta = round(delta_value, 2))
                st.markdown(f"<p style ='font-size:0.75rem;'>₱ {round(prev,2)}/s ({str(self.current_datetime.year-1)})</p>", unsafe_allow_html=True)

            with cols[1]:
                st.metric(f"%YLD to Date",f"{round(curr/(float(curr_price.strip('%')))*100,2)}%", f"{round(curr/(float(curr_price.strip('%')))*100 - float(prev_percent.strip('%')),2)}%")
                st.markdown(f"<p style ='font-size:0.75rem;'>{prev_percent} ({str(self.current_datetime.year-1)})</p>", unsafe_allow_html=True)

            with cols[2]:
                if ticker_name is not None:
                    with st.spinner("Fetching Data..."):
                        req = threading.Thread(target=self.load_equity_data())
                        req.start()
                        req.join()


        except Dividend_Data_Error as e:
            st.error(f"{ticker_name} does not have an updated Dividend Data. Consider other dividend stocks.")
            st.session_state["error_message"] = e

        except AttributeError as e:
            if ticker_name is None:
                st.info('Choose dividend stock to view.')
            else:
                st.error('Problem with Data Parser')
                st.session_state["error_message"] = e

    def view_all_dividend_info(self, ticker_name):
        self.div_data = self.DATA.get_dividend_data(st.session_state['stock_on_view'])
        df = pd.DataFrame.from_dict(self.div_data['div_data'], orient="index",columns=['Year','Type','Rate','ExDate','RecordDate','PaymentDate'])
        st.markdown("<p style='font-align:justify;'>Showing More Dividend Information</p>",unsafe_allow_html=True)
        st.table(df)
        st.write(f"<p style ='font-size:0.75rem;'>Data from: <a href='www.pesobility.com'>www.pesobility.com",unsafe_allow_html=True )
             
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
                    st.markdown('<p style="font-size:1rem; font-family:Arial; color:#03045e;">Logged in as: <span style="color:#03045e;font-size:1rem; font-family:Monospace;font-weight:bold;">GUEST</span></p>', unsafe_allow_html=True)
                    st.caption("<p style='color:#200E3A'>Login or register an account.", unsafe_allow_html=True)
                else:
                    st.header("*VIEWING THE PROFILE IF LOGGED IN*")

    def custom_selection(self):
        if not st.session_state["logged-in"]:
            stockPick = st.selectbox(
                    'Choose what Dividend Stock to View',
                    self.TOML.get_PSE_list(),index=None,
                    help='Choose what Dividend Stock to show. Make sure the stock ticker is valid.')
            
            st.session_state['stock_on_view'] = stockPick
            return stockPick
        
        else:
            stockPick = st.multiselect(
                    'View Annual Dividend Data',
                    self.TOML.get_PSE_list(),
                    self.TOML.get_stockpicks(), max_selections= 5,
                    help='Choose what Stock Dividends to show')
            st.session_state['stock_on_view'] = stockPick

            return stockPicks
        
    def pre_section_body1(self):
        st.divider()
        st.image("resources\dividend_watch2.png", use_column_width=True)

    def section_body1(self):
        if not st.session_state["logged-in"]:
            try:
                self.pre_section_body1()
                stocks = self.custom_selection()
                with st.sidebar:
                    st.header(":gear: Additional Settings")

                    if stocks is None:
                        disable=True
                    elif stocks is not None:
                        disable=False

                    show_div_data = st.checkbox("Show Dividend Data", value=True, disabled=disable)
                    show_all_dividend_data = st.checkbox("Show Addl. Dividend Data", disabled=disable)

                if show_div_data and st.session_state['stock_on_view'] is not None:           
                    with st.container(border=True):
                        st.markdown(f'''<p style="font-size: 2rem; text-align: center; font-family: Arial;"> {stocks} - {self.TOML.get_company_name(stocks)[0]}</p>''', unsafe_allow_html=True)
                        self.create_columns(stocks)
                if show_all_dividend_data and st.session_state['stock_on_view'] is not None:
                    with st.container(border=True):
                        self.view_all_dividend_info(stocks)

            except TypeError as e:
                st.info(f'Choose stock to view') 
                st.session_state["error_message"] = e

            except ValueError as e:
                #Problems with some pref shares values
                st.error("A persisting error with Preferred Shares are still being fixed.")
                st.info("Consider other dividend stocks.")
                st.session_state["error_message"] = e

            except Dividend_Data_Error as e:
                #The error notice was handled inside the first container
                st.session_state["error_message"] = e
                pass


            except Equity_Data_Error(st.session_state["stock_on_view"]) as e:
                    #exception handled
                    # st.warning("There are errors gathering equity data")
                    pass
            

            with st.sidebar:
                with st.container(border=True):
                    st.write(st.session_state['error_message'])