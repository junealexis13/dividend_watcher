import streamlit as st
from scripts.configs import TOML


class UI:
    def __init__(self) -> None:
        #instantiate configs
        self.TOML = TOML()
        self.cols = self.TOML.get_stockpicks()

    def create_columns(self):
        col_nums = len(self.cols)
        
        #create cols
        cols = st.columns(col_nums)

        #iterate through cols created
        for col_name, col in zip(self.cols, cols):
            with col:
                st.header(col_name)
    