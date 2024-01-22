import pandas as pd
import streamlit as st
import os, re, datetime

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
            "bday"          : self.bday,
            "gender"        : self.gender
        }
    
    def get_full_address(self):
        return f"{self.brgy}, {self.citymuni}, {self.prov}, {self.reg}"
    
