import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "stocks.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ✅ Create alerts table
cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    alert_type TEXT,
    stock_symbol TEXT,
    condition TEXT,
    value REAL,
    status TEXT DEFAULT 'active'
)
""")

conn.commit()
conn.close()

print("✅ Alerts table created successfully!")