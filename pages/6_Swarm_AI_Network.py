import streamlit as st
import requests
import plotly.graph_objects as go
import networkx as nx
import random

st.title("🧠 ULTRA SWARM AI NETWORK")

COORD = "http://127.0.0.1:9100/api/nodes"

data = requests.get(COORD).json()
nodes = data["nodes"]

G = nx.Graph()
G.add_node("BRAIN")

for n in nodes:
    G.add_node(n["node_id"])
    G.add_edge("BRAIN", n["node_id"])

pos = nx.spring_layout(G, seed=7)

edge_x = []
edge_y = []

for e in G.edges():
    x0,y0 = pos[e[0]]
    x1,y1 = pos[e[1]]

    edge_x += [x0,x1,None]
    edge_y += [y0,y1,None]

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    mode='lines',
    line=dict(width=3,color='cyan'),
    opacity=0.4
)

node_x=[]
node_y=[]
colors=[]
sizes=[]
labels=[]

for node in G.nodes():

    x,y=pos[node]
    node_x.append(x)
    node_y.append(y)

    if node=="BRAIN":
        colors.append("cyan")
        sizes.append(50)
        labels.append("Coordinator Brain")
    else:
        info = next((n for n in nodes if n["node_id"]==node),None)
        alive = info.get("alive",False)

        colors.append("lime" if alive else "red")
        sizes.append(30)

        labels.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=labels,
    textposition="bottom center",
    marker=dict(
        size=sizes,
        color=colors
    )
)

fig = go.Figure(data=[edge_trace,node_trace])

fig.update_layout(
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
)

st.plotly_chart(fig, use_container_width=True)
