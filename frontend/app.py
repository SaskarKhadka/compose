import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Hello World Logs")

try:
    res = requests.get(f"{API_URL}/logs")
    res.raise_for_status()
    logs = res.json()

    if logs:
        for log in logs:
            st.write(f"{log['timestamp']}: {log['message']}")
    else:
        st.info("No logs found.")
except Exception as e:
    st.error(f"Failed to fetch logs: {e}")