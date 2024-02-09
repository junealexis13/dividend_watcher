import toml, os, json
from datetime import datetime
import hashlib
import streamlit as st
from supabase import create_client, Client
from typing import Literal
from scripts.app_state import STATE


class SB_CLIENT:
    def __init__(self) -> None:
        self.SB_URL = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        self.SB_KEY = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]

        #Init Client
        self.SB_Client: Client = create_client(self.SB_URL, self.SB_KEY)

        self.CONFIGS = STATE()

    def register_User(self, email: str, password: str, data: dict, *args):

        res = self.SB_Client.auth.sign_up(
            {
                "email": email,
                "password" : password,
                "options": {
                    "data": data
                }
            }
        )

    def signIn_User(self, email: str, password: str , *args):
        data = self.SB_Client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
    
        st.session_state['logged-in'] = True
        self.fetch_all_user_sp()
        self.fetch_all_user_wallet()
        self.fetch_all_user_transactions()

    def signOut(self):
        try:
            res = self.SB_Client.auth.sign_out()
            st.session_state["logged-in"] = False

            with open(os.path.join("user_cookies.toml"),"w") as sp:
                toml.dump({"stockPicks":[]},sp)

            self.CONFIGS.__init_states() #reset

            
        except Exception as e:
            st.error(e)

    def create_stockPicks(self, stockpicks: list, stockpick_name: str):
        jsonize_stockpicks = json.dumps(stockpicks)
        self.SB_Client.table("stockpicks").insert({"picks": jsonize_stockpicks, "sp_name": stockpick_name}).execute()
        self.fetch_all_user_sp()

    def update_stockPicks(self, stockpicks: list, stockpick_name: str, sp_id: str):
        jsonize_stockpicks = json.dumps(stockpicks)
        self.SB_Client.table("stockpicks").update({"picks": jsonize_stockpicks,"sp_name":stockpick_name}).eq("SP_id",sp_id).execute()
        self.fetch_all_user_sp()
        
    def fetch_all_user_sp(self):
        data = self.SB_Client.table("stockpicks").select("sp_name","picks","SP_id").eq("id",self.fetch_user_info("id")).execute()
        update_picks = {"stockPicks":data.data}

        with open(os.path.join("user_cookies.toml"),'w') as sp:        
            toml.dump(update_picks,sp)
            sp.close()

        #default behavior. there is a mechanism to update this tho
        st.session_state["active_stockPicks"] = json.loads(data.data[0]['picks'])

    def create_sp_rows(self):
        get_sp = toml.load(os.path.join("user_cookies.toml"))

    def fetch_user_info(self, fetch_type="md"):
        data = self.SB_Client.auth.get_user()
        user_dict = dict(data)['user']
        
        if st.session_state["user_metadata"] is None:
            st.session_state["user_metadata"] = user_dict.user_metadata

        match fetch_type:
            case "md":
                return user_dict.user_metadata
            case "id":
                return user_dict.id


    def create_selection(self):
        try:
            with open(os.path.join("user_cookies.toml"),"r") as rd:
                toml_sp = toml.load(rd)
                picks = toml_sp['stockPicks']
                sel_picks = st.selectbox("Set active Stockpicks",index=0,options=[x["sp_name"] for x in picks])
                selection = [d for d in picks if d['sp_name'] == sel_picks]
                set_sp = json.loads(selection[0]["picks"])
                if st.session_state["active_stockPicks"] is not None:
                    st.session_state["active_stockPicks"] = set_sp
                rd.close()
        except IndexError as e:
             #error present if the user is logged out.
             pass
        
    def select_sp_element(self):
        if st.session_state["logged-in"]:
            with open(os.path.join("user_cookies.toml"),"r") as rd:
                toml_sp = toml.load(rd)
                picks = toml_sp['stockPicks']
                sel_picks = st.selectbox("Set Stockpick",index=0,options=[x["sp_name"] for x in picks])
                selection = [d for d in picks if d['sp_name'] == sel_picks]
                rd.close()
                return selection[0]

    def create_wallet(self, wallet_name: str):
        self.SB_Client.table("Wallet").insert({"wallet_name": wallet_name}).execute()
        self.fetch_all_user_wallet()

    def fetch_all_user_wallet(self):
        data = self.SB_Client.table("Wallet").select("*").eq("user_id",self.fetch_user_info("id")).execute()
        update_picks = {"wallet":data.data}

        if len(update_picks) != 0 or data is not None:
            st.session_state["user_wallet"] = update_picks

    def fetch_all_user_transactions(self):
        data = self.SB_Client.table("Stocks_Transactions").select("tx_id","equity","tx_type","pps","tx_date","volume").eq("id",self.fetch_user_info("id")).execute()
        update_picks = {"user_transactions":data.data}

        if len(update_picks) != 0 or data is not None:
            st.session_state["user_transactions"] = update_picks

    def create_user_transactions(self,tx_type: Literal["buy", "sell"], equity: str, price_per_share: float, volume: int, wallet_id: str):
        self.SB_Client.table("Stocks_Transactions").insert({"wallet": wallet_id, "pps":price_per_share, "tx_type": tx_type, "equity": equity, "volume":volume
                                                            , "id": self.fetch_user_info("id")}).execute()
        self.fetch_all_user_wallet()