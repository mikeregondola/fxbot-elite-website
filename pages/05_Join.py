import streamlit as st
import json

cfg=json.load(open("config_web.json"))

st.title("Join FXBot Elite")

st.markdown(f"""
Pay via:

👉 PayPal: {cfg["paypal_link"]}

👉 GCash: {cfg["gcash_number"]}

👉 Crypto Wallet:
{cfg["crypto_wallet"]}
""")
