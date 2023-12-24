import pandas as pd
import requests
from exceptions import *
from bs4 import BeautifulSoup


class StockData:
    def __init__(self) -> None:
        #Allows to request info from PESOBILITY
        self.address = "http://www.pesobility.com/"
        self.div_address = "https://www.pesobility.com/dividends"
        self.url_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        self.temp_data = {}

    def get_dividend_data(self, stock_code: str):
        a = requests.get(self.div_address + f"/{stock_code.upper()}", headers=self.url_headers)
        soup = BeautifulSoup(a.content, 'lxml')
        elem = soup.find( "div", {"id": "MAIN_BODY"})
        data = elem.find_all("td")

        #Take note that the data structure was identified as [Year,Dividend Type,Rate,Ex-Dividend Date,Record Date,Payment Date]
        
        #check first if the data is divisible by 6

        if len(data)%6==0:
            for i, div_data in enumerate(data):
                if i%6==0:
                    self.temp_data[len(self.temp_data) + 1] = [x.text.strip("<td>/") for x in data[i:i+6]]

        else:
            raise Data_Structure_Error()

        if len(self.temp_data) > 0:
            return {"stock_code" : stock_code, "div_data": self.temp_data}
        elif len(self.temp_data) == 0:
            raise Dividend_Data_Error()