import pandas as pd
import requests
import re
import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from scripts.exceptions import *
from bs4 import BeautifulSoup



class StockData:
    def __init__(self) -> None:
        #Allows to request info from PESOBILITY
        self.address = "http://www.pesobility.com/"
        self.div_address = "https://www.pesobility.com/dividends"
        self.url_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}


        self.current_datetime = datetime.now()
        self.current_market_stat_address = "https://phisix-api2.appspot.com/stocks.json"
        self.current_stock_stat_address = "https://phisix-api2.appspot.com/stocks/"

    def get_dividend_data(self, stock_code: str):
        self.temp_data = {}
        a = requests.get(self.div_address + f"/{stock_code.upper()}", headers=self.url_headers)
        soup = BeautifulSoup(a.content, 'lxml')


        #Get Main Data
        elem = soup.find( "div", {"id": "MAIN_BODY"})
        data = elem.find_all("td")

        #Get Percentage
        get_labels = soup.find_all("label")

        #Get current Price
        curr_price = get_labels[0].text
        loc_str_price = re.search(r'\d+(\.\d+)?', curr_price)

        if loc_str_price:
            curr_prce_pershare = loc_str_price.group()
        else:
            raise Dividend_Data_Error(message="DDE1.2")


        #Take note that the data structure was identified as [Year,Dividend Type,Rate,Ex-Dividend Date,Record Date,Payment Date]
        #check first if the data is divisible by 6

        if len(data)%6==0:
            for i, div_data in enumerate(data):
                if i%6==0:
                    self.temp_data[len(self.temp_data) + 1] = [re.sub(r'\.(.*?)\.', r'.\1', x.text.strip("<td>/"))  for x in data[i:i+6]]
        else:
            raise Data_Structure_Error

        if len(self.temp_data) > 0:
            return {"stock_code" : stock_code, "curr_price": curr_prce_pershare, "div_data": self.temp_data}
        elif len(self.temp_data) == 0:
            raise Dividend_Data_Error(message='DDE1.3')

    def pack_dividend_data(self, stock_code):
        div_data = self.get_dividend_data(stock_code=stock_code)
        dft = pd.DataFrame.from_dict(div_data["div_data"],orient="index", columns=['Year','Type','Rate','ExDate','RecordDate','PaymentDate'])

        if self.current_datetime.year not in dft['Year'].unique():
            _year = self.current_datetime.year - 1
            _prev_year = self.current_datetime.year - 2
        else:
            _year = self.current_datetime.year
            _prev_year = self.current_datetime.year - 1
            
        current_div_data = dft.loc[(dft["Year"] == str(_year)) & (dft["Type"] == "Cash")]
        current_total_div = sum([float(re.sub(r'[^\d.]', '', x)) for x in current_div_data["Rate"]])

        prev_div_data = dft.loc[(dft["Year"] == str(_prev_year)) & (dft["Type"] == "Cash")]
        prev_total_div = sum([float(re.sub(r'[^\d.]', '', x)) for x in prev_div_data["Rate"]])
        prev_percent =  round(prev_total_div / float(div_data["curr_price"]),3)
        
        return current_total_div, prev_total_div, div_data["curr_price"], prev_percent, _year
    
    def get_stock_stats(self, ticker_name):
        try:
            if ticker_name is not None:
                req = requests.get(self.current_stock_stat_address + f"{ticker_name}.json")
                mquote = req.json()
                return mquote
            else:
                return None
        except Exception as e:
            raise Equity_Data_Error(ticker_name)
    