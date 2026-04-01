import sqlite3
import os
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "stocks.db")


# -----------------------------
# CREATE ALERT
# -----------------------------
def create_alert(alert):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO alerts (user_id, alert_type, stock_symbol, condition, value, status)
        VALUES (?, ?, ?, ?, ?, 'active')
    """, (
        alert["user_id"],
        alert["alert_type"],
        alert["stock_symbol"],
        alert["condition"],
        alert["value"]
    ))

    conn.commit()
    conn.close()


# -----------------------------
# GET ALERTS
# -----------------------------
def get_alerts():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM alerts")
    alerts = cur.fetchall()

    conn.close()
    return alerts


# -----------------------------
# DELETE ALERT
# -----------------------------
def delete_alert(alert_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM alerts WHERE id=?", (alert_id,))
    conn.commit()
    conn.close()


# -----------------------------
# 🔥 GET LIVE STOCK PRICE
# -----------------------------
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="1d")

        if data.empty:
            return None

        return float(data["Close"].iloc[-1])
    except:
        return None


# -----------------------------
# 🔥 ALERT EVALUATION LOGIC
# -----------------------------
def evaluate_alerts():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, stock_symbol, condition, value 
        FROM alerts 
        WHERE status='active'
    """)

    alerts = cur.fetchall()
    triggered = []

    for alert in alerts:
        alert_id, symbol, condition, value = alert

        current_price = get_stock_price(symbol)

        if current_price is None:
            continue

        if condition == "above" and current_price > value:
            triggered.append({
                "id": alert_id,
                "stock": symbol,
                "price": current_price
            })

        elif condition == "below" and current_price < value:
            triggered.append({
                "id": alert_id,
                "stock": symbol,
                "price": current_price
            })

    conn.close()
    return triggered