import sqlite3
import uuid
from datetime import datetime

DB = "members.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id TEXT PRIMARY KEY,
        email TEXT,
        tier TEXT,
        payment_status TEXT,
        node_id TEXT,
        join_date TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_member(email, tier):

    member_id = str(uuid.uuid4())
    node_id = "node-" + uuid.uuid4().hex[:6]

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        INSERT INTO members VALUES (?,?,?,?,?,?)
    """,(member_id,email,tier,"PAID",node_id,str(datetime.now())))

    conn.commit()
    conn.close()

    return node_id
