import sqlite3

conn = sqlite3.connect(r"C:\Users\lakes\OneDrive\Desktop\stock_api_project\stocks.db")
cursor = conn.cursor()

# Create table if not exists (SAFE)
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

# Clear old data (optional)
cursor.execute("DELETE FROM stocks")

# Insert fresh data (IMPORTANT)
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

cursor.executemany("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

conn.commit()
conn.close()

print("DB FULLY RESET ✅")