import streamlit as st
import requests

st.title("Stock Alert Dashboard")

# ✅ Use your deployed backend URL
API_URL = "https://stock-screener-4a85.onrender.com"

if st.button("Check Alerts"):
    try:
        res = requests.get(f"{API_URL}/alerts/check")
        
        if res.status_code == 200:
            data = res.json()

            if data.get("triggered_alerts"):
                for alert in data["triggered_alerts"]:
                    st.success(alert)
            else:
                st.info("No alerts triggered")
        else:
            st.error("Failed to fetch alerts")

    except Exception as e:
        st.error(f"Backend error: {e}")
