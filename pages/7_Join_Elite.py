import streamlit as st
from member_engine import create_member

st.title("🚀 Join FXBot Elite Network")

st.markdown("""
Become part of the decentralized Wave 3 trading network.

Select your participation tier below.
""")

# -----------------------------
# Tier Selection
# -----------------------------

tier = st.selectbox(
    "Select Membership Tier",
    [
        "Lite Node (Passive participant)",
        "Trader Node (Active trading)",
        "Elite Operator (Full control)"
    ]
)

email = st.text_input("Email Address")

device_name = st.text_input(
    "Optional Device Name (Mini-PC name)",
    placeholder="ex: mini-pc-1"
)

# -----------------------------
# Join Button
# -----------------------------

if st.button("JOIN ELITE NETWORK"):

    if email.strip() == "":
        st.error("Email required.")
        st.stop()

    # Create member automatically
    member = create_member(
        email=email,
        tier=tier,
        device_name=device_name
    )

    st.success("🎉 Membership Created!")

    st.markdown("### Your Member Credentials")

    st.code(f"""
Member ID: {member['id']}
Tier: {member['tier']}
Status: {member['status']}
""")

    st.markdown("### Next Step")

    st.info("""
1️⃣ Copy your MEMBER ID.

2️⃣ Place it inside your Mini-PC config:

