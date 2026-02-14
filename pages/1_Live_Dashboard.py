import streamlit as st
import requests

COORD = "http://127.0.0.1:9100"

st.title("📊 Live Coordinator Dashboard")

try:
    r = requests.get(f"{COORD}/api/nodes", timeout=3)
    data = r.json()

    st.metric("Total Capital", data["total_capital"])
    st.metric("Active W3", data["active_w3"])

    for n in data["nodes"]:
        st.write(n)

except:
    st.error("Coordinator offline.")
