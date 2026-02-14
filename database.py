import sqlite3

DB="fxbot_members.db"

def get_db():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    db=get_db()
    c=db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        tier TEXT,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS nodes(
        id INTEGER PRIMARY KEY,
        user_email TEXT,
        node_id TEXT,
        last_seen INTEGER
    )
    """)

    db.commit()
