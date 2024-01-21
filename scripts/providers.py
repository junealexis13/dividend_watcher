import streamlit as st
from eod import EodHistoricalData
import json, os
from datetime import datetime, timedelta
from supabase import create_client, Client
# from scripts.configs import *

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
    
    def update_data(self):
        a = open(os.path.join("temp","data.json"),"r")
        load_json = json.load(a)
        a.close()
        updated_json = {}
        dates = []
        for data in load_json.values():
            try:
                #take not that by default, the data is ascending
                if data[-1]['date'] not in dates:
                    dates.append(datetime.strptime((data[-1]['date']), "%Y-%m-%d"))
            except IndexError:
                # "Stock is halted,terminated, or inactive."
                pass

        from_when=max(dates) + timedelta(days=1)
        to_when=datetime.now().date()

        ####

        for data in load_json.items():
            update = self.get_historical_prices(data[0].strip(),from_date=from_when,to_date=to_when)
            updated_json[data[0]] = data[1] + update

        update_data = open(os.path.join("temp","data.json"),"w")
        json.dump(updated_json,update_data,indent=2)
            



if __name__ == "__main__":
    a = DATA_PROVIDERS()
    a.update_data()
