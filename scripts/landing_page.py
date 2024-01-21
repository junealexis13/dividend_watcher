import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import threading
import toml, requests, os, json, requests
import numpy as np
from datetime import datetime
from scripts.configs import TOML
from scripts.data_parser import StockData
from scripts.app_state import STATE
from scripts.exceptions import *
from scripts.providers import DATA_PROVIDERS

class UI:
    def __init__(self) -> None:
        #instantiate configs
        self.SessionStates = STATE()
        self.TOML = TOML()
        self.DATA = StockData()
        self.cols = self.TOML.get_stockpicks()
        self.current_datetime = datetime.now()
        self.providers = DATA_PROVIDERS()
        
    def login_ui(self):
        with st.container(border=True):
            st.markdown("<p style='color: black;'>Account Login</p>", unsafe_allow_html=True)
            user_login = st.text_input(label="user",type="default")
            user_pass = st.text_input(label="password",type="password")
            return user_login, user_pass
        
    def load_equity_data(self):
        self.PSE_stats = self.DATA.get_stock_stats(st.session_state['stock_on_view']) 
        data_stock = self.PSE_stats['stock'][0]
        st.metric("Current Equity Data",f"₱{data_stock['price']['amount']}",f"{data_stock['percent_change']}%")
        st.markdown(f"<p style ='font-size:0.75rem;'>Latest Vol. {int(data_stock['volume']):,}</p>", unsafe_allow_html=True)

    def fetch_3month_stream(self, ticker_name):
        return self.DATA.create_historical_data(ticker_name)
    
    def create_columns(self, ticker_name):
        #create cols
        col_nums = 3
        cols = st.columns(col_nums)

        #iterate through cols created
        try:
            #Fetch the info in PD Form
            curr, prev, curr_price, prev_percent, yr = self.DATA.pack_dividend_data(ticker_name)
            delta_value = curr - prev

            #Create year variables
            if yr != str(self.current_datetime.year):
                _year = self.current_datetime.year - 1
                _prev_year = self.current_datetime.year -2
            else:
                _year = self.current_datetime.year
                _prev_year = self.current_datetime.year - 1


            with cols[0]:
                st.metric(f"DV YLD ({str(_year)}) ",f"₱{round(curr,2)}/s", delta = round(delta_value, 2))
                st.markdown(f"<p style ='font-size:0.75rem;'>₱ {round(prev,2)}/s ({str(_prev_year)})</p>", unsafe_allow_html=True)

            with cols[1]:
                st.metric(f"%YLD to Date",f"{round(curr/(float(curr_price.strip('%')))*100,2)}%", f"{round((curr/(float(curr_price.strip('%'))))*100 - (prev_percent*100),2)}%")
                st.markdown(f"<p style ='font-size:0.75rem;'>{prev_percent*100}% ({str(_prev_year)})</p>", unsafe_allow_html=True)


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
        st.write(f"<p style ='font-size:0.75rem;'>Data from: <a href='http://www.pesobility.com/dividends/{ticker_name.upper()}', target='_blank'>www.pesobility.com",unsafe_allow_html=True )
             
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
                st.image(os.path.join("resources","user.png"), use_column_width = True, caption='user')

            with col2:
                if not st.session_state['logged-in']:
                    st.markdown('<p style="font-size:1rem; font-family:Arial; color:#03045e;">Logged in as: <span style="color:#03045e;font-size:1rem; font-family:Monospace;font-weight:bold;">GUEST</span></p>', unsafe_allow_html=True)
                    st.caption("<p style='color:#200E3A'>Login or register an account.", unsafe_allow_html=True)
                else:
                    st.header("*VIEWING THE PROFILE IF LOGGED IN*")

    def custom_selection(self):
        stockPick = st.selectbox(
                'Choose what Dividend Stock to View',
                self.TOML.get_PSE_list(),index=None,
                help='Choose what Dividend Stock to show. Make sure the stock ticker is valid.')
        
        st.session_state['stock_on_view'] = stockPick
        return stockPick

    def pre_section_body1(self):
        st.divider()
        st.image(os.path.join("resources","dividend_watch2.png"), use_column_width=True)

    def pre_section_body2(self):
        st.divider()
        st.image(os.path.join("resources","equity_header.png"), use_column_width=True)

    def section_body1(self):
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
                    st.markdown(f'''<p style="font-size: 2rem; text-align: center; font-family: Arial;"> {stocks} - {self.TOML.get_company_name(stocks)}</p>''', unsafe_allow_html=True)
                    self.create_columns(stocks)
            if show_all_dividend_data and st.session_state['stock_on_view'] is not None:
                with st.container(border=True):
                    self.view_all_dividend_info(stocks)
                    st.write(self.fetch_3month_stream(stocks))

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

        except Equity_Data_Error as e:
                #exception handled
                # st.warning("There are errors gathering equity data")
                pass
            
    def section_body2(self):
        obj = Section_Objects()
        self.pre_section_body2()

        #Stock picks section
        st.divider()
        st.markdown(f"<h1 style='text-align: center;padding-top: 0;'> Watchlist</h1>", unsafe_allow_html=True)
        if not st.session_state['logged-in']:
            st.caption("<p style='text-align: center;padding: 0;'>You are not logged in. Register an account and see your favorite stocks here.</p>", unsafe_allow_html=True)
        elif st.session_state['logged-in']:
            stockPicks = obj.fetch_stockpicks(typeOut='sp')
            obj.create_watchlist(len(stockPicks)//3,len(stockPicks)%3,stockPicks, typeOut="sp")
        st.divider()

        #View Active Stocks section
        st.markdown(f"<h1 style='text-align: center;padding-top: 0;'> Equity Viewer</h1>", unsafe_allow_html=True)
        activePicks = obj.fetch_stockpicks(typeOut="ac") #typeOut reflects the type of fetch_ command

        obj.create_watchlist(len(activePicks)//3,len(activePicks)%3,activePicks,typeOut="ac")

    def section_body3(self):
        run = st.button(label="Update current price data")
        
        if run:
            with st.spinner("Fetching all 1yr data..."):
                self.providers.update_data()
            st.info("Dataset updated")


class Section_Objects:
    def __init__(self) -> None:
        #Fetch recent market data
        self.DATA = StockData()
        self.TOML = TOML()

    def fetch_stockpicks(self, typeOut="sp"):
        if typeOut.lower() == 'sp':
            with open("user_cookies.toml", "r") as rd :
                load_cookies = toml.load(rd)
                rd.close()
            return load_cookies["stockPicks"]
        
        if typeOut.lower() == 'ac':
            stock_picks = st.multiselect("Select multiple stocks to view",self.TOML.get_PSE_list(), max_selections=9, help="You can select up to 9 stocks at the same time.")
            return stock_picks
        
    def create_cols(self, length):
        cols = st.columns(length)
        return cols

    def create_equity_card(self, ticker_symbol, idTag=None):
        @st.cache_data
        def get_market_stats():
            req = requests.get("https://phisix-api2.appspot.com/stocks.json")
            mquote = req.json()
            return mquote
        
        with st.container(border=True):
            name = self.TOML.get_company_name(ticker_symbol, truncate=True, max_len = 22)
            st.markdown(f'''<p style="font-size: 0.75vw; text-align: center; font-family: Arial;">{name}</p>''', unsafe_allow_html=True)

            for search_eqt in get_market_stats()['stock']:
                if ticker_symbol.upper() == search_eqt['symbol']:
                    if search_eqt['percent_change'] > 0:
                        ticker_color = "#1eedd1"
                    elif search_eqt['percent_change'] < 0:
                        ticker_color = "#ff4d4d"
                    elif search_eqt['percent_change'] == 0:
                        ticker_color = "#d9d9d9"
                    value = int(search_eqt['price']['amount']*search_eqt['volume'])
                    st.markdown('''<html>
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai+Looped:wght@100;200;300;500;600;700&display=swap" rel="stylesheet">
    <style>
        #price {
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            font-weight: 700;
            font-size: 2vw;
            text-align: center;
            margin-bottom: 1px; /* Adjust the margin between paragraphs */
        }
        
        #change {
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            font-weight: 500;
            font-size: 1vw;
            text-align: center;
            margin-top: 1px; /* Adjust the margin between paragraphs */
            color: *tick_color*;
            padding: 0;
        }
                                
        #ticker_[ticker_tag] {
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            padding: 0;
            text-align: center;
            color: [ticker_color];
            font-weight:500;
        }
                                
        #volume_[ticker_tag] {
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            padding: 0;
            text-align: center;
            font-weight:200;
            font-size: 0.65rem;
        }
        #divider_p {
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            padding: 0;
            text-align: center;
            font-weight:800;
            font-size:0.5rem;
        }                            
        #value_view{
            font-family: 'IBM Plex Sans Thai Looped', sans-serif;
            padding: 0;
            text-align: center;
            font-weight:400;
            font-size: 0.75rem;
        }
        .reduce_margin{
            margin-bottom: 0;
        }            


    </style>
</head>
<body>
    <div class="cont">
        <p id="price">%price%</p>
        <p id="ticker_[ticker_tag]">%percent_change%</p>
        <p id="divider_p" class="reduce_margin">Intra-day Volume & Value</p>
        <p id="value_view" class="reduce_margin"><b>%value%</b></p>     
        <p id="volume_[ticker_tag]"><b>%volume%</b> [symbol]</p>
    </div>
                   
</body>
</html>

                                '''.replace("[symbol]",ticker_symbol.upper()).replace("%price%",f"₱{search_eqt['price']['amount']}").replace("%value%",f"₱{value:,}").replace("%percent_change%",f"{search_eqt['percent_change']}%").replace("%volume%",f"{int(search_eqt['volume']):,}").replace("[ticker_tag]",f"{idTag}").replace("[ticker_color]", ticker_color),unsafe_allow_html=True)
                    break
                
    def create_watchlist(self, full_rows, partial_rows, stockpicks, typeOut=None):
            '''
            Pass row specs and stockpicks to create watchlist grid
            '''
            match full_rows, partial_rows:
                case full_rows, 0:
                    for i in range(full_rows):
                        cols = self.create_cols(3)
                        for n, col in enumerate(cols):
                            with col:
                                if typeOut.lower() == "sp":
                                    self.create_equity_card(stockpicks[i*3+n],idTag=f"sp{i*3+n}")
                                elif typeOut.lower() == "ac":
                                    self.create_equity_card(stockpicks[i*3+n],idTag=f"ac{i*3+n}")
                case full_rows, partial_rows if partial_rows > 0:
                    #fetch full rows
                    for i in range(full_rows):
                        cols = self.create_cols(3)
                        for n, col in enumerate(cols):
                            with col:
                                if typeOut.lower() == "sp":
                                    self.create_equity_card(stockpicks[i*3+n],idTag=f"sp{i*3+n}")
                                elif typeOut.lower() == "ac":
                                    self.create_equity_card(stockpicks[i*3+n],idTag=f"ac{i*3+n}")
                    
                    #Fetch the last rows which was incomplete
                    part_cols = self.create_cols(partial_rows)
                    for n, col in enumerate(part_cols):
                        with col:
                            if typeOut.lower() == "sp":
                                self.create_equity_card(stockpicks[full_rows*3+n], idTag=f"sp{full_rows*3+n}")
                            elif typeOut.lower() == "ac":
                                self.create_equity_card(stockpicks[full_rows*3+n], idTag=f"ac{full_rows*3+n}")
