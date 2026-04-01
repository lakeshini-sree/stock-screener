import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>

/* 🌐 Import Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* 🔤 GLOBAL FONT */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
}

/* 🧠 TITLES */
h1 {
    font-size: 40px !important;
    font-weight: 700;
}
h2, h3 {
    font-size: 24px !important;
}

/* 📊 METRIC CARDS */
[data-testid="stMetric"] {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
}

/* 📊 METRIC TEXT */
[data-testid="stMetricValue"] {
    font-size: 28px !important;
}

/* 📥 INPUTS */
input, textarea {
    font-size: 18px !important;
}

/* 🔘 BUTTON */
.stButton>button {
    font-size: 18px !important;
    padding: 10px 20px !important;
    border-radius: 10px;
}

/* 📊 TABLE */
.stDataFrame {
    font-size: 16px !important;
}

/* 📂 SIDEBAR */
section[data-testid="stSidebar"] * {
    font-size: 18px !important;
}

/* 💡 SUCCESS BOX */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 StockAI Dashboard")

page = st.sidebar.radio("Navigation", [
    "🔍 Screener",
    "💼 Portfolio",
    "🚨 Alerts"
])

# ---------------- SESSION ----------------
if "results" not in st.session_state:
    st.session_state["results"] = None

# ==============================
# 🔍 SCREENER
# ==============================
if page == "🔍 Screener":

    st.markdown("<h1>📈 Smart Stock Screener</h1>", unsafe_allow_html=True)

    query = st.text_input("Enter your query")

    if st.button("Search"):
        try:
            res = requests.post(f"{BASE_URL}/query", json={"query": query})
            st.session_state["results"] = res.json()
        except:
            st.error("❌ Backend not running")

    if st.session_state["results"] and st.session_state["results"]["status"] == "success":

        data = st.session_state["results"]["data"]["results"]
        df = pd.DataFrame(data)

        st.success(f"✅ {len(df)} Stocks Found")

        if not df.empty:

            # KPI
            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Avg Price", f"₹{int(df['price'].mean())}")
            col2.metric("📊 Avg Revenue", f"{int(df['revenue'].mean())}")
            col3.metric("📈 Avg Profit", f"{int(df['profit'].mean())}")

            # Top stock
            top = df.sort_values(by="profit", ascending=False).iloc[0]

            st.markdown("### 🏆 Top Performing Stock")
            st.info(f"{top['company']} | Price: ₹{top['price']} | Profit: {top['profit']}")

            # Tabs
            tab1, tab2 = st.tabs(["📋 Table", "📈 Charts"])

            with tab1:
                st.dataframe(df, use_container_width=True)

            with tab2:
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Price Comparison")
                    st.bar_chart(df.set_index("company")["price"])

                with col2:
                    st.subheader("Profit Comparison")
                    st.bar_chart(df.set_index("company")["profit"])

# ==============================
# 💼 PORTFOLIO
# ==============================
elif page == "💼 Portfolio":

    st.markdown("<h1>💼 Portfolio Tracker</h1>", unsafe_allow_html=True)

    st.info("Track your investments")

    col1, col2, col3 = st.columns(3)

    stock = col1.text_input("Stock Name")
    buy_price = col2.number_input("Buy Price", value=0)
    current_price = col3.number_input("Current Price", value=0)

    if st.button("Calculate"):

        profit = current_price - buy_price

        st.markdown("### 📊 Result")

        if profit > 0:
            st.success(f"Profit: ₹{profit}")
        elif profit < 0:
            st.error(f"Loss: ₹{profit}")
        else:
            st.warning("No profit, no loss")

# ==============================
# 🚨 ALERTS
# ==============================
elif page == "🚨 Alerts":

    st.markdown("<h1>🚨 Smart Alerts</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    user_id = col1.text_input("User ID", "user1")
    stock = col2.text_input("Stock Symbol")

    col3, col4 = st.columns(2)

    condition = col3.selectbox("Condition", ["above", "below"])
    price = col4.number_input("Target Price")

    if st.button("Set Alert"):
        try:
            requests.post(f"{BASE_URL}/alerts", json={
                "user_id": user_id,
                "alert_type": "price",
                "stock_symbol": stock,
                "condition": condition,
                "value": price
            })
            st.success("✅ Alert created successfully!")
        except:
            st.error("❌ Backend not running")

    st.markdown("---")

    if st.button("Check Alerts"):
        try:
            res = requests.get(f"{BASE_URL}/alerts/check")
            data = res.json()

            if data.get("status") == "success":
                alerts = data.get("triggered_alerts", [])

                if alerts:
                    st.success("🚀 Triggered Alerts")
                    st.table(pd.DataFrame(alerts))
                else:
                    st.info("No alerts triggered")
            else:
                st.error(data.get("error", {}).get("message", "Error"))

        except:
            st.error("❌ Backend not running")
