import pandas as pd
import numpy as np
import streamlit as st
import os, re, datetime, toml
from typing import Literal

class ADDRESS_TOOLS:
    '''
    Manages the quick selection view and automatic update of places
    '''
    def __init__(self) -> None:
        self.add_index = pd.read_csv(os.path.join("resources","ph_address_index.csv"), encoding='ISO-8859-1', sep=";")

    def get_regions(self):
        return list(self.add_index['adm1'].unique())
    
    def get_province(self, index_rgn: str):
        indexed_provinces = self.add_index.loc[self.add_index["adm1"] == index_rgn]
        return list(indexed_provinces["adm2"].unique())

    def get_city_muni(self, index_prv: str):
        indexed_city_muni = self.add_index.loc[self.add_index["adm2"] == index_prv]
        return list(indexed_city_muni["adm3"].unique())
    
    def get_brgy(self, index_city_muni: str):
        indexed_brgy = self.add_index.loc[self.add_index["adm3"] == index_city_muni]
        return list(indexed_brgy["adm4"].unique())
    
class USER_INFO_MNGR:
    '''
    Class for Handling user inputs during acct creation
    '''
    def __init__(self, fname, lname, reg, prov, citymuni, brgy, bday: datetime.date, gender) -> None:
        self.fname = fname
        self.lname = lname
        self.reg = reg
        self.prov = prov
        self.citymuni = citymuni
        self.brgy = brgy
        self.bday = str(bday)
        self.gender = gender

    def pack_data(self):
        return {
            "first_name"    : self.fname,
            "last_name"     : self.lname,
            "add_reg"       : self.reg,
            "add_prov"      : self.prov,
            "add_citymuni"  : self.citymuni,
            "add_brgy"      : self.brgy,
            "birthday"      : self.bday,
            "gender"        : self.gender
        }
    
    def get_full_address(self):
        return f"{self.brgy}, {self.citymuni}, {self.prov}, {self.reg}"
    
class TECHNICAL_ANALYSIS_TOOLS:
    '''
    Useful tools for calculating several TA indicators
    '''

    def __init__(self) -> None:
        pass

    def calc_RSI(self, data: pd.Series):
        price_action = data['close'].diff()
        price_up = price_action.copy()
        price_down = price_action.copy()

        price_up[price_up<0] = 0
        price_down[price_down>0] = 0

        avg_up = price_up.rolling(14).mean()
        avg_down = price_down.rolling(14).mean().abs()

        return 100 - (100 / (1 + (avg_up/avg_down)))
    
class OTHERS:
    def __init__(self) -> None:
        pass

    def write_trans(self, tx_type: Literal['buy','sell'], equity: str, volume: int, pps: float, dt: str):
        if tx_type == "buy":
            st.write(f":moneybag::moneybag: -- Bought {equity} | Volume: {volume} | Price: {pps} | Value: {volume*pps} | Transaction Date: {dt}")
        elif tx_type == "sell":
            st.write(f":money_with_wings::money_with_wings: -- Bought {equity} | Volume: {volume} | Price: {pps} | Value: {volume*pps} | Transaction Date: {dt}")