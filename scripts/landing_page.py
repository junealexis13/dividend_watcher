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
    
    def introduction(self):
        st.caption('''<!DOCTYPE html>
<html>
<head>
<style>
p {
  text-align: justify;
}
</style>
</head>
<body>

<p>
Welcome to the Dividend Screener app, your go-to platform for tracking and analyzing dividends listed on the Philippine Stock Exchange. Our app is designed to help you make informed investment decisions by providing real-time data, comprehensive screening tools, and in-depth analysis of companies offering dividends. Whether you’re a seasoned investor or just starting out, the Dividend Screener app is an essential tool for anyone looking to invest in dividend stocks in the Philippines. Start your journey towards smarter investing today with the Dividend Screener app!
</p>

</body>
</html>
''', unsafe_allow_html=True)
        
        