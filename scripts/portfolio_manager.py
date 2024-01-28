import streamlit as st
from scripts.appAuth import *
import toml, os
from supabase import create_client, Client

class PORTFOLIO_MANAGER(SB_CLIENT):
    def __init__(self):
        self.SB_URL = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        self.SB_KEY = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]

        #Init Client
        self.newClient: Client = create_client(self.SB_URL, self.SB_KEY)