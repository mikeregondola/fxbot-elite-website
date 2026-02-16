import json
import uuid
import os
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------

DATA_DIR = "data"
MEMBER_DB = os.path.join(DATA_DIR, "members.json")

# -----------------------------
# INIT DATABASE
# -----------------------------

def ensure_db():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(MEMBER_DB):

        db = {
            "members": []
        }

        with open(MEMBER_DB, "w") as f:
            json.dump(db, f, indent=2)


# -----------------------------
# LOAD / SAVE
# -----------------------------

def load_members():

    ensure_db()

    with open(MEMBER_DB, "r") as f:
        return json.load(f)


def save_members(db):

    with open(MEMBER_DB, "w") as f:
        json.dump(db, f, indent=2)


# -----------------------------
# CREATE MEMBER
# -----------------------------

def create_member(email, tier, device_name=None):

    db = load_members()

    member_id = str(uuid.uuid4())[:8]

    member = {
        "id": member_id,
        "email": email,
        "tier": tier,
        "device_name": device_name,
        "status": "pending",   # pending → active
        "created": datetime.utcnow().isoformat()
    }

    db["members"].append(member)

    save_members(db)

    return member


# -----------------------------
# GET MEMBER
# -----------------------------

def get_member(member_id):

    db = load_members()

    for m in db["members"]:
        if m["id"] == member_id:
            return m

    return None


# -----------------------------
# ACTIVATE MEMBER
# (used after payment confirmation later)
# -----------------------------

def activate_member(member_id):

    db = load_members()

    for m in db["members"]:

        if m["id"] == member_id:
            m["status"] = "active"
            save_members(db)
            return m

    return None


# -----------------------------
# LIST MEMBERS (Dashboard use)
# -----------------------------

def list_members():

    db = load_members()
    return db["members"]
