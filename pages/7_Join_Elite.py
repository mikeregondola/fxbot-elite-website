import streamlit as st
import requests
import uuid
import json

st.title("🚀 Join FXBot Elite Network")

st.write("Register your account and join the autonomous trading cluster.")

# ---- Member Inputs ----

name = st.text_input("Your Name")
email = st.text_input("Email")

tier = st.selectbox(
    "Choose Tier",
    ["Tier 1 - Observer", "Tier 2 - Trader", "Tier 3 - Node Provider"]
)

if st.button("Join Elite"):

    member_id = str(uuid.uuid4())

    payload = {
        "member_id": member_id,
        "name": name,
        "email": email,
        "tier": tier
    }

    try:
        requests.post(
            "https://YOUR-COORDINATOR-URL/register_member",
            json=payload,
            timeout=3
        )

        st.success(f"Welcome! Your Member ID: {member_id}")

    except Exception:
        st.warning("Coordinator offline. Saved locally.")

        with open("pending_members.json","a") as f:
            f.write(json.dumps(payload) + "\n")
