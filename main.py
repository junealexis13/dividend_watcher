from configs import TOML
from data_parser import StockData

if __name__ == "__main__":
    A = TOML()
    print(A.get_stockpicks())
    print("After Editing...")
    A.config_edit("update","AP","X")
    print(A.get_stockpicks())
    # B = StockData()
    # print(B.get_dividend_data(stock_picks[2]))