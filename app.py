import streamlit as st
import json

# ----------------------------------
# CONFIG
# ----------------------------------

MEMBERS_FILE = "members.json"

# ----------------------------------
# LOAD MEMBERS
# ----------------------------------

def load_members():
    try:
        with open(MEMBERS_FILE) as f:
            return json.load(f)["members"]
    except:
        return []

members = load_members()

# ----------------------------------
# UI HEADER
# ----------------------------------

st.set_page_config(page_title="FXBot Elite Control Panel")

st.title("🚀 FXBot Elite Platform")

# ----------------------------------
# MEMBER LOGIN
# ----------------------------------

st.sidebar.header("Member Login")

member_id = st.sidebar.text_input("Enter Member ID")

member = None

for m in members:
    if m["member_id"] == member_id and m.get("active", False):
        member = m
        break

if not member:
    st.warning("Enter valid Member ID")
    st.stop()

tier = member["tier"]

st.sidebar.success(f"Logged in as: {member_id}")
st.sidebar.write(f"Tier: {tier}")

# ----------------------------------
# TIER ENGINE
# ----------------------------------

def has_role(role):
    return role in member.get("allowed_roles", [])

# ----------------------------------
# DASHBOARD
# ----------------------------------

st.header("Dashboard")

st.write("Member Tier:", tier)

if has_role("viewer"):
    st.success("Dashboard Access Enabled")

# ----------------------------------
# NODE PANEL
# ----------------------------------

if has_role("lite_node"):
    st.header("🖥 Lite Node Control")

    st.write("Your PC can join execution cluster.")

    if st.button("Join Cluster"):
        st.success("Node ready (auto discovery enabled)")

# ----------------------------------
# PRO SIGNALS PANEL
# ----------------------------------

if tier in ["elite", "authority"]:
    st.header("📊 Elite Signal Access")

    st.info("W3 signals available here.")

# ----------------------------------
# AUTHORITY PANEL
# ----------------------------------

if tier == "authority":
    st.header("🧠 Authority Controls")

    st.write("Full system monitoring enabled.")

# ----------------------------------
# FOOTER
# ----------------------------------

st.markdown("---")
st.caption("FXBot Elite Infrastructure")
