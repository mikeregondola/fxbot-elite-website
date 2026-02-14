import streamlit as st
import requests
import json

cfg=json.load(open("config_web.json"))

st.title("Member Dashboard")

try:
    data=requests.get(f"{cfg['coordinator_url']}/api/nodes").json()
    st.json(data)
except:
    st.error("Coordinator offline")
