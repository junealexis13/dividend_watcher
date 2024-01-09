import toml, os
import hashlib
import streamlit as st
from supabase import create_client, Client


class SB_CLIENT:
    def __init__(self) -> None:
        self.SB_URL = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
        self.SB_KEY = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]

        #Init Client
        self.SB_Client: Client = create_client(self.SB_URL, self.SB_KEY)

    def register_User(self, email: str, password: str, data: dict, *args):

        def encrypt_password(password = password):
            encrypted_pword = hashlib.sha256(password.encode()).hexdigest()
            return encrypted_pword

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

        return data

    def signOut(self):
        try:
            res = self.SB_Client.auth.sign_out()
            st.session_state["logged-in"] = False
            st.rerun()
        except Exception as e:
            st.error(e)