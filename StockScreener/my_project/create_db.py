import sqlite3
import os

# -----------------------------
# DB PATH (FIXED)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Creating database at:", DB_PATH)

# -----------------------------
# CREATE STOCKS TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY,
    company TEXT,
    sector TEXT,
    revenue INTEGER,
    price INTEGER,
    market_cap INTEGER,
    quarter TEXT,
    profit INTEGER
)
""")

# -----------------------------
# CLEAR OLD DATA (SAFE RESET)
# -----------------------------
cursor.execute("DELETE FROM stocks")

# -----------------------------
# INSERT SAMPLE DATA
# -----------------------------
data = [
    (1, "TCS", "IT", 120000, 450, 1500000, "Q1", 20000),
    (2, "Infosys", "IT", 110000, 420, 1200000, "Q1", 18000),
    (3, "HDFC", "Finance", 90000, 1500, 900000, "Q1", 15000),
    (4, "Reliance", "Energy", 200000, 2500, 2000000, "Q1", 25000),
    (5, "Wipro", "IT", 80000, 380, 700000, "Q1", 12000),

    (6, "TCS", "IT", 140000, 480, 1600000, "Q2", 25000),
    (7, "Infosys", "IT", 115000, 430, 1250000, "Q2", 20000),
    (8, "HDFC", "Finance", 95000, 1550, 950000, "Q2", 17000),
    (9, "Reliance", "Energy", 210000, 2600, 2100000, "Q2", 30000),
    (10, "Wipro", "IT", 85000, 400, 750000, "Q2", 15000)
]

cursor.executemany("""
INSERT INTO stocks (id, company, sector, revenue, price, market_cap, quarter, profit)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", data)

# -----------------------------
# CREATE ALERTS TABLE
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    alert_type TEXT,
    stock_symbol TEXT,
    condition TEXT,
    value REAL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# -----------------------------
# 🔥 ADD INDEXES (OPTIMIZATION)
# -----------------------------
cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON stocks(price)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_sector ON stocks(sector)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_profit ON stocks(profit)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_revenue ON stocks(revenue)")

# -----------------------------
# COMMIT + CLOSE
# -----------------------------
conn.commit()
conn.close()

print("✅ Database created successfully with indexes!")