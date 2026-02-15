import streamlit as st

st.set_page_config(page_title="Authority Architecture", layout="wide")

st.title("🏛️ FXBot Elite Distributed Trading Architecture")

st.markdown("""
Institutional-grade autonomous trading infrastructure designed
for distributed execution, capital efficiency, and advanced
risk coordination.
""")

# ----------------------
# Architecture Diagram
# ----------------------

st.header("System Architecture")

st.markdown("""
Signal Brain (PRO Engine)
        ↓
Coordinator Brain
        ↓
Execution Nodes (Lite PCs)
        ↓
Broker Execution Layer
""")

# ----------------------
# DAO-like Execution Model
# ----------------------

st.header("Decentralized Execution Model")

st.markdown("""
FXBot Elite uses a distributed execution network where:

- Signals originate from the PRO engine.
- Coordinator manages capital exposure and global locks.
- Lite nodes execute trades independently.
- Risk is isolated per node.
""")

# ----------------------
# Technical Advantages
# ----------------------

st.header("Technical Advantages")

st.markdown("""
- Global W3 coordination lock
- ATR-timed risk release
- Autonomous node routing
- Broker-agnostic design
- Distributed capital scaling
- Failover-ready architecture
""")

# ----------------------
# Comparison
# ----------------------

st.header("Why FXBot Elite Is Different")

st.table({
"Traditional Signal Groups": [
"Manual execution",
"Single account risk",
"Human decision latency",
"Copy trading delays"
],
"FXBot Elite": [
"Automated distributed execution",
"Distributed capital structure",
"Algorithmic coordination",
"Direct node execution"
]
})

# ----------------------
# Whitepaper Download
# ----------------------

st.header("Authority Documentation")

st.download_button(
    label="Download Architecture Whitepaper",
    data=open("assets/FXBot_Elite_Authority_Architecture_Whitepaper.pdf","rb").read(),
    file_name="FXBot_Elite_Architecture_Whitepaper.pdf"
)
