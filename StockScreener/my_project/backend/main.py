import os
import sys
import sqlite3
import re
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# -----------------------------
# FIX IMPORT PATH
# -----------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# -----------------------------
# IMPORTS
# -----------------------------
# ✅ CORRECT IMPORTS
from StockScreener.my_project.backend.services.llm_service import nl_to_dsl
from StockScreener.my_project.backend.services.validator import validate_dsl
from StockScreener.my_project.backend.services.alerts_service import (
    create_alert,
    get_alerts,
    delete_alert,
    evaluate_alerts
)
from compiler.query_builder import SQLCompiler

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI()

# -----------------------------
# DB PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "stocks.db")

print("🔥 USING DB:", DB_PATH)

# -----------------------------
# CREATE TABLES (AUTO FIX)
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # alerts table
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
    print("✅ DB initialized")

init_db()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MODELS
# -----------------------------
class QueryRequest(BaseModel):
    query: str

class AlertRequest(BaseModel):
    user_id: str
    alert_type: str
    stock_symbol: str
    condition: str
    value: float

# -----------------------------
# HELPERS
# -----------------------------
def execute_query(sql_query, values):
    start = time.time()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(sql_query, values)
    rows = cursor.fetchall()

    conn.close()

    execution_time = round(time.time() - start, 6)

    return [dict(row) for row in rows], execution_time


# -----------------------------
# TEST ROUTE
# -----------------------------
@app.get("/")
def home():
    return {"message": "Backend working ✅"}


# -----------------------------
# QUERY API
# -----------------------------
@app.post("/query")
def query_endpoint(request: QueryRequest):
    try:
        dsl = {"conditions": [], "logic": "AND"}
        user_query = request.query

        # Quarter detection
        quarter_match = re.search(r'\bq([1-4])\b', user_query.lower())
        if quarter_match:
            dsl["conditions"].append({
                "field": "quarter",
                "operator": "=",
                "value": f"Q{quarter_match.group(1)}"
            })

        # NLP → DSL
        nl_dsl = nl_to_dsl(user_query)
        dsl["conditions"].extend(nl_dsl.get("conditions", []))

        validate_dsl(dsl)

        # SQL compile
        compiler = SQLCompiler(dsl)
        sql_query, values = compiler.build_query()

        # Execute
        results, exec_time = execute_query(sql_query, values)

        return {
            "status": "success",
            "execution_time": exec_time,
            "data": {
                "natural_query": user_query,
                "dsl_query": dsl,
                "sql_query": sql_query,
                "results": results
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# -----------------------------
# ALERT APIs
# -----------------------------
@app.post("/alerts")
def add_alert(alert: AlertRequest):
    try:
        create_alert(alert.dict())
        return {"status": "success", "message": "Alert created"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/alerts")
def fetch_alerts():
    try:
        return {"status": "success", "alerts": get_alerts()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.delete("/alerts/{alert_id}")
def remove_alert(alert_id: int):
    try:
        delete_alert(alert_id)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/alerts/check")
def check_alerts():
    try:
        triggered = evaluate_alerts()
        return {
            "status": "success",
            "triggered_alerts": triggered
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
