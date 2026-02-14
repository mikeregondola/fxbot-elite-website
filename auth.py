import streamlit as st

def login_ui():

    email=st.text_input("Email")
    password=st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state["user"]=email
        st.success("Logged in")
