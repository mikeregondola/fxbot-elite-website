import streamlit as st
import requests

st.set_page_config(page_title="Elite Control Center", layout="wide")

st.title("🧠 FXBot Elite Control Center")

# ----------------------
# CONFIG
# ----------------------

COORDINATOR_URL = "http://127.0.0.1:9100/api/nodes"

# ----------------------
# Fetch data
# ----------------------

try:
    r = requests.get(COORDINATOR_URL, timeout=3)
    data = r.json()

except Exception as e:
    st.error("Coordinator unreachable.")
    st.stop()

# ----------------------
# Overview
# ----------------------

st.header("Network Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Capital", data.get("total_capital",0))
col2.metric("Active W3 Lock", data.get("active_w3","None"))
col3.metric("Node Count", len(data.get("nodes",[])))

# ----------------------
# Node Table
# ----------------------

st.header("Execution Nodes")

nodes = data.get("nodes",[])

if nodes:

    table = []

    for n in nodes:

        table.append({
            "Node": n["node_id"],
            "IP": n["ip"],
            "Mode": n["mode"],
            "Capital": n["capital"],
            "Symbols": ",".join(n["symbols"]),
            "Alive": n["alive"],
            "Trades": n["stats"]["total"],
            "Winrate": n["stats"]["winrate"],
            "Equity": n["equity"].get("current")
        })

    st.dataframe(table)

else:

    st.info("No nodes connected.")

# ----------------------
# System Health
# ----------------------

st.header("System Health")

if data.get("active_w3"):
    st.warning("W3 Lock Active")
else:
    st.success("No Active Lock")

st.caption("Live data pulled from Coordinator API.")
