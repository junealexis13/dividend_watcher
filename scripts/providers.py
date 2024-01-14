import streamlit as st
from eod import EodHistoricalData
import json, os
from supabase import create_client, Client
from scripts.configs import *

class DATA_PROVIDERS:

    def __init__(self) -> None:
        self.url: str = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        self.key: str = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
        self.sb: Client = create_client(self.url, self.key)

    def data_upload(self,stock_data: dict, ticker_symbol: str):
        ###
        if "warning" in stock_data.keys():
            pass
        else:
            self.sb.table(f"stock_info_{ticker_symbol}").insert(stock_data).execute()

    def get_historical_prices(self,ticker_symbol, from_date, to_date) -> list:
        client = EodHistoricalData(st.secrets["eodhd"]["API_KEY"])
        resp = client.get_prices_eod(f'{ticker_symbol.upper()}.PSE', period='a', order='a', from_=from_date, to = to_date )

                # [self.data_upload(quote, ticker_symbol=ticker_symbol) for quote in resp]
        return resp