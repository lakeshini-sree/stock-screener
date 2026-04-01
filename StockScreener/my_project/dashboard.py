import streamlit as st
import requests

st.title("Stock Alert Dashboard")

if st.button("Check Alerts"):
    res = requests.get("http://127.0.0.1:8000/alerts/check")
    data = res.json()

    for alert in data["triggered_alerts"]:
        st.write(alert)