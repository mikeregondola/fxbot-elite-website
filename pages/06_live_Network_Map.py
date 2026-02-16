import streamlit as st
import requests
import plotly.graph_objects as go
import networkx as nx

st.title("📡 ULTRA LIVE NETWORK MAP")

COORD_URL = "http://127.0.0.1:9100/api/nodes"

# --- fetch coordinator data ---
try:
    data = requests.get(COORD_URL).json()
    nodes = data.get("nodes", [])
except:
    st.error("Coordinator not reachable")
    st.stop()

# --- build graph ---
G = nx.Graph()

# coordinator brain
G.add_node("COORDINATOR")

for n in nodes:
    nid = n["node_id"]
    G.add_node(nid)
    G.add_edge("COORDINATOR", nid)

# layout
pos = nx.spring_layout(G, seed=42)

# edges
edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]

    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=2),
    hoverinfo='none',
    mode='lines'
)

# nodes
node_x = []
node_y = []
text = []
colors = []
sizes = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

    if node == "COORDINATOR":
        colors.append("cyan")
        sizes.append(40)
        text.append("Coordinator Brain")
    else:
        info = next((n for n in nodes if n["node_id"]==node), None)

        alive = info.get("alive", False)
        symbols = ",".join(info.get("symbols", []))

        colors.append("lime" if alive else "red")
        sizes.append(25)

        text.append(f"{node}<br>{symbols}")

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=text,
    textposition="bottom center",
    marker=dict(
        size=sizes,
        color=colors,
        line=dict(width=2)
    )
)

fig = go.Figure(data=[edge_trace, node_trace])

fig.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
)

st.plotly_chart(fig, use_container_width=True)
