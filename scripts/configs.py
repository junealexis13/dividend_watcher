import toml, os, re, glob
import pandas as pd
from scripts.exceptions import *

class TOML:
    def __init__(self) -> None:
        self.working_path = os.getcwd()
        self.conf_toml = glob.glob(os.path.join(self.working_path,"user_cookies.toml"))
        self.listed_companies = "resources/listed_company_directory.csv"

    def get_PSE_list(self, mode = "ticker" ):
        df = pd.read_csv(self.listed_companies, delimiter="|")
        # return ticker set 
        if mode.lower() == "ticker":
            return list(df['symbol'])
        elif mode.lower() == "name":
            return list(df["company_name"])
        elif mode.lower() == "all":
            return df[['symbol','company_name']]       
        else:
            raise Mode_Error
        
    def config_load(self) -> dict:
        config_data = toml.load(self.conf_toml)
        return config_data
    
    def get_stockpicks(self) -> str:
        return self.config_load()['stockPicks']
    
    def get_company_name(self, ticker_symbol):
        try:
            df = self.get_PSE_list("all")
            comp_name = df.loc[df["symbol"] == ticker_symbol.upper()]
            return comp_name["company_name"].values
        
        except AttributeError:
            print("Empty Input")
        
    def config_edit(self, edit_mode, *new_stock_pics):
        #Check the stockpicks first
        for comps in new_stock_pics:
            if comps.upper() not in self.get_PSE_list():
                raise Company_Info_Error(comps.upper())
                break

        try:
            match edit_mode.lower():
                case "overwrite":
                    with open(self.conf_toml[0],"w") as rd:
                        toml.dump({"stockpicks": list(new_stock_pics)}, rd)
                        rd.close()

                case "append" | "update":
                    new_picks = set(self.get_stockpicks() + list(new_stock_pics))
                    with open(self.conf_toml[0],"w") as rd:
                        toml.dump({"stockPicks": sorted(list(new_picks))}, rd)
                        rd.close()
                        
                case other:
                    raise Edit_Mode_Error
                
        except KeyError as e:
            #add an empty stockpicks list in case there is a keyerror
            with open(self.conf_toml[0],"w") as rd:
                toml.dump({"stockPicks": list()}, rd)
                rd.close()
    
