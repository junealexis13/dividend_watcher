import streamlit as st
# from scripts.exceptions import *
import toml, os

class PORTFOLIO_MANAGER:
    def __init__(self):
        pass

    def get_stockpicks(self):
        try:
            stock_picks = toml.load(os.path.join("user_cookies.toml"))
            return stock_picks['stockPicks']
        except KeyError as e:
            return list()

    def edit_stockpicks(self, new_stockpicks: list):
        with open(os.path.join("user_cookies.toml"),"w") as rd:
            toml.dump({"stockPicks":{new_stockpicks}})

if __name__ == "__main__":
    A = PORTFOLIO_MANAGER()
    print(A.get_stockpicks())