import streamlit as st
from eod import EodHistoricalData
import json
from supabase import create_client, Client


def data_upload(stock_data: dict, ticker_symbol: str):
    url: str = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
    key: str = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    sb: Client = create_client(url, key)

    ###
    if "warning" in stock_data.keys():
        pass
    else:
        sb.table(f"stock_info_{ticker_symbol}").insert(stock_data).execute()

    


def get_historical_prices(ticker_symbol, from_date, to_date, dump=False):
    client = EodHistoricalData(st.secrets["eodhd"]["API_KEY"])
    st.write("Client succefully initialized!")
    resp = client.get_prices_eod(f'{ticker_symbol.upper()}.PSE', period='a', order='a', from_=from_date, to = to_date )
    if dump:
        with st.spinner("Dumping files to Data Server"):
            [data_upload(quote, ticker_symbol=ticker_symbol) for quote in resp]
if __name__ == "__main__":
    
    fromdate = st.date_input("Start Date")
    todate = st.date_input("To Date")
    ticker = st.text_input("Ticker Symbol", max_chars=3)
    run = st.button(label="Run request")
    if run:
        req = get_historical_prices(ticker.upper(),fromdate.strftime('%Y-%m-%d'), todate.strftime('%Y-%m-%d'), dump=True)
        st.write("Dumped files. Please check the DB.")