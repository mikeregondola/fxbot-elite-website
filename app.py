import time
import json
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

STATE_FILE = "coordinator_state.json"
MEMBER_DB = "members.db"

# --------------------------------
# ROLE MAP
# --------------------------------

TIER_ROLE_MAP = {
    "tier1": "viewer",
    "tier2": "signal",
    "tier3": "contributor",
    "elite": "master"
}

# --------------------------------
# DEFAULT STATE
# --------------------------------

def default_state():
    return {
        "locks": {},
        "active_w3": None,
        "nodes": {},
        "total_capital": 0,
        "symbol_pool": ["EURUSD","GBPUSD","USDJPY"],
        "max_symbols_per_node": 1
    }

def load_state():
    try:
        with open(STATE_FILE,"r") as f:
            return json.load(f)
    except:
        return default_state()

def save_state(state):
    with open(STATE_FILE,"w") as f:
        json.dump(state,f,indent=2)

state = load_state()

# --------------------------------
# MEMBER VALIDATION (NEW)
# --------------------------------

def validate_member(node_id):

    try:
        conn = sqlite3.connect(MEMBER_DB)
        c = conn.cursor()

        c.execute("SELECT tier FROM members WHERE node_id=?",(node_id,))
        row = c.fetchone()

        conn.close()

        if row:
            tier = row[0]
            role = TIER_ROLE_MAP.get(tier,"viewer")
            return True, tier, role

    except Exception as e:
        print("[MEMBER DB ERROR]",e)

    return False, None, None

# --------------------------------
# HEALTH
# --------------------------------

@app.route("/health")
def health():
    return jsonify({
        "status":"ok",
        "nodes":len(state["nodes"]),
        "active_w3":state["active_w3"]
    })

# --------------------------------
# NODE REGISTER (UPDATED)
# --------------------------------

@app.route("/register", methods=["POST"])
def register():

    data = request.json
    node_id = data.get("node_id")

    if not node_id:
        return jsonify({"ok":False,"reason":"NO_NODE_ID"})

    # NEW: membership validation
    valid, tier, role = validate_member(node_id)

    if not valid:
        return jsonify({"ok":False,"reason":"INVALID_MEMBER"})

    ip = request.remote_addr

    state["nodes"][node_id] = {
        "ip": ip,
        "tier": tier,
        "role": role,
        "last_seen": int(time.time()),
        "allowed_symbols": []
    }

    save_state(state)

    print(f"[REGISTER] {node_id} → {tier} ({role})")

    return jsonify({
        "ok":True,
        "node_id":node_id,
        "tier":tier,
        "role":role
    })

# --------------------------------
# HEARTBEAT
# --------------------------------

@app.route("/heartbeat", methods=["POST"])
def heartbeat():

    data = request.json
    node_id = data.get("node_id")

    if node_id in state["nodes"]:
        state["nodes"][node_id]["last_seen"] = int(time.time())
        save_state(state)

    return jsonify({"ok":True})

# --------------------------------
# SYMBOL ASSIGNMENT (ROLE AWARE)
# --------------------------------

@app.route("/assignment/<node_id>")
def assignment(node_id):

    if node_id not in state["nodes"]:
        return jsonify({"ok":False})

    node = state["nodes"][node_id]

    # viewer cannot trade
    if node["role"] == "viewer":
        return jsonify({"ok":True,"symbols":[]})

    # contributor / master auto assign
    if not node["allowed_symbols"]:

        used = set()
        for n in state["nodes"].values():
            used.update(n.get("allowed_symbols",[]))

        for sym in state["symbol_pool"]:
            if sym not in used:
                node["allowed_symbols"] = [sym]
                break

        if not node["allowed_symbols"]:
            node["allowed_symbols"] = [state["symbol_pool"][0]]

        save_state(state)

    return jsonify({
        "ok":True,
        "symbols":node["allowed_symbols"],
        "role":node["role"]
    })

# --------------------------------
# W3 LOCK
# --------------------------------

@app.route("/request_w3", methods=["POST"])
def request_w3():

    data = request.json
    symbol = data.get("symbol")

    if state["active_w3"] is None:
        state["active_w3"] = symbol
        state["locks"][symbol] = {"ts":int(time.time())}
        save_state(state)
        return jsonify({"ok":True})

    return jsonify({"ok":False})

@app.route("/release_w3", methods=["POST"])
def release_w3():

    data = request.json
    symbol = data.get("symbol")

    if symbol in state["locks"]:
        del state["locks"][symbol]

    if state["active_w3"] == symbol:
        state["active_w3"] = None

    save_state(state)

    return jsonify({"ok":True})

# --------------------------------

if __name__ == "__main__":
    print("[COORD] Elite Auto Role Engine ENABLED")
    app.run(host="0.0.0.0",port=9100)
