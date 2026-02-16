import streamlit as st
import json

DB = "data/members.json"

st.title("Member Login")

email = st.text_input("Email")

if st.button("Login"):

    with open(DB,"r") as f:
        data = json.load(f)

    for m in data["members"]:
        if m["email"] == email:
            st.session_state.member = m
            st.success("Logged in")
