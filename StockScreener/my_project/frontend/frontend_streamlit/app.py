import streamlit as st
import pandas as pd
import random

st.set_page_config(layout="wide")

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    font-size: 18px;
}

h1 {
    font-size: 40px !important;
    font-weight: 700;
}
h2, h3 {
    font-size: 24px !important;
}

[data-testid="stMetric"] {
    background-color: #111827;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    font-size: 28px !important;
}

.stButton>button {
    font-size: 18px !important;
    padding: 10px 20px !important;
    border-radius: 10px;
}

.stDataFrame {
    font-size: 16px !important;
}

section[data-testid="stSidebar"] * {
    font-size: 18px !important;
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

import requests

# ==============================
# 🔍 SCREENER (CONNECTED TO BACKEND)
# ==============================
if page == "🔍 Screener":

    st.markdown("<h1>📈 Smart Stock Screener</h1>", unsafe_allow_html=True)

    query = st.text_input("Enter your query (ex: revenue > 100000, Q1)")

    if st.button("Search"):

        try:
            response = requests.post(
    "https://your-backend.onrender.com/query",
    json={"query": query}
)
            result = response.json()

            if result["status"] == "success":
                data = result["data"]["results"]

                if len(data) == 0:
                    st.warning("No data found")
                else:
                    df = pd.DataFrame(data)
                    st.session_state["results"] = df

            else:
                st.error(result["message"])

        except Exception as e:
            st.error(f"Backend not running ❌\n{e}")

    if st.session_state["results"] is not None:

        df = st.session_state["results"]

        st.success(f"✅ {len(df)} Stocks Found")

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Avg Price", f"₹{int(df['price'].mean())}")
        col2.metric("📊 Avg Revenue", f"{int(df['revenue'].mean())}")
        col3.metric("📈 Avg Profit", f"{int(df['profit'].mean())}")

        top = df.sort_values(by="profit", ascending=False).iloc[0]

        st.markdown("### 🏆 Top Performing Stock")
        st.info(f"{top['company']} | Price: ₹{top['price']} | Profit: {top['profit']}")

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
        st.success("✅ Alert saved (demo mode)")

    if st.button("Check Alerts"):
        st.info("No alerts triggered (demo mode)")
