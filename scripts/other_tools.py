import pandas as pd
import streamlit as st
import os, re

class ADDRESS_TOOLS:
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
    
