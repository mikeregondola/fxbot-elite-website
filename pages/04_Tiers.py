import streamlit as st

st.set_page_config(layout="wide")

st.title("💼 Elite Membership Structure")

tiers = [
    ("🟢 Tier 1 — Observer",
     ["Education library",
      "W3 strategy training",
      "Weekly commentary",
      "Delayed signals"]),
      
    ("🔵 Tier 2 — Active Trader",
     ["Live W3 signals",
      "Risk automation tools",
      "Elite dashboard",
      "Personal execution control"]),
      
    ("🔴 Tier 3 — Node Operator",
     ["Run Lite node",
      "Auto execution",
      "Cluster participation",
      "Priority signals"]),
      
    ("🟣 Tier 4 — Elite Authority",
     ["Institutional analytics",
      "DAO governance",
      "Cloud cluster access",
      "Advanced strategy beta"])
]

cols = st.columns(4)

for col, tier in zip(cols, tiers):
    with col:
        st.subheader(tier[0])
        for item in tier[1]:
            st.write("✔", item)
