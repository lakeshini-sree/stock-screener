import sqlite3
import os
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "stocks.db")

# -----------------------------
# CREATE ALERT
# -----------------------------
def create_alert(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO alerts (user_id, alert_type, stock_symbol, condition, value)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["user_id"],
        data["alert_type"],
        data["stock_symbol"],
        data["condition"],
        data["value"]
    ))

    conn.commit()
    conn.close()

# -----------------------------
# GET ALERTS
# -----------------------------
def get_alerts():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM alerts")
    rows = cur.fetchall()

    conn.close()

    return [dict(row) for row in rows]

# -----------------------------
# DELETE ALERT
# -----------------------------
def delete_alert(alert_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM alerts WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()

# -----------------------------
# CHECK ALERTS
# -----------------------------
def evaluate_alerts():
    alerts = get_alerts()
    triggered = []

    for alert in alerts:
        try:
            stock = yf.Ticker(alert["stock_symbol"])
            price = stock.history(period="1d")["Close"].iloc[-1]

            if alert["condition"] == ">" and price > alert["value"]:
                triggered.append(f"{alert['stock_symbol']} above {alert['value']}")
            elif alert["condition"] == "<" and price < alert["value"]:
                triggered.append(f"{alert['stock_symbol']} below {alert['value']}")

        except:
            continue

    return triggered
