import streamlit as st
import requests
import plotly.graph_objects as go
import random

st.title("🌐 Swarm AI Network")

# -----------------------------
# CONFIG
# -----------------------------

def get_coord_url():

    # Cloud deployment
    if "COORDINATOR_URL" in st.secrets:
        return st.secrets["COORDINATOR_URL"]

    # Local fallback
    return "http://127.0.0.1:9100"


COORD = get_coord_url()

# -----------------------------
# FETCH DATA
# -----------------------------

def load_nodes():

    try:
        r = requests.get(f"{COORD}/api/nodes", timeout=3)
        return r.json()

    except:
        st.warning("Coordinator offline — Demo mode enabled")

        # demo fallback
        return {
            "nodes":[
                {"node_id":"mini-pc-1","member_id":"member_A","capital":5000},
                {"node_id":"mini-pc-2","member_id":"member_B","capital":3000},
                {"node_id":"mini-pc-3","member_id":"member_A","capital":2500}
            ]
        }


data = load_nodes()
nodes = data.get("nodes", [])

# -----------------------------
# BUILD VISUAL GRAPH
# -----------------------------

if len(nodes) == 0:

    st.info("No nodes registered.")
    st.stop()

fig = go.Figure()

x_nodes = []
y_nodes = []
labels = []
colors = []
sizes = []

for n in nodes:

    x_nodes.append(random.random())
    y_nodes.append(random.random())

    member = n.get("member_id","unknown")

    labels.append(
        f"{n['node_id']}<br>Member:{member}<br>Capital:{n.get('capital',0)}"
    )

    colors.append(hash(member) % 10)

    sizes.append(20 + n.get("capital",0)/200)

fig.add_trace(go.Scatter(
    x=x_nodes,
    y=y_nodes,
    mode='markers+text',
    text=[n["node_id"] for n in nodes],
    hovertext=labels,
    marker=dict(
        size=sizes,
        color=colors,
        showscale=False
    )
))

fig.update_layout(
    showlegend=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TABLE VIEW
# -----------------------------

st.subheader("Node Details")

st.dataframe(nodes)
