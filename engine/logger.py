import sqlite3
from datetime import datetime

def log_scan(target, score):
    conn = sqlite3.connect("phishguard.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            score INTEGER,
            created TIMESTAMP
        )
    """)
    c.execute(
        "INSERT INTO scans (target, score, created) VALUES (?, ?, ?)",
        (target, score, datetime.utcnow())
    )
    conn.commit()
    conn.close()
