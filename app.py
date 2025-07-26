import streamlit as st
import pandas as pd
from datetime import datetime

# Name/title
st.title("Artifact RNG Pattern Tracker")

st.header("Log a new upgrade event")

with st.form("upgrade_form"):
    # Artifact substats may have 0-4 lines
    artifact_type = st.selectbox("Artifact type", ["0-line", "1-line", "2-line", "3-line", "4-line"])
    
    # Upgrade target (line added or increased)
    upgraded_line = st.selectbox("Which line received the upgrade (or was added)?", [1, 2, 3, 4])

    # Upgrade milestone (e.g. +3, +6, etc.)
    upgrade_level = st.selectbox("Upgrade level", ["+3", "+6", "+9", "+12", "+15"])

    # Submit entry
    submitted = st.form_submit_button("Add Entry")

# In-memory upgrade log (lives until app restarts)
if "upgrade_log" not in st.session_state:
    st.session_state.upgrade_log = []

# Save new entry to log
if submitted:
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.upgrade_log.append({
        "timestamp": timestamp,
        "artifact_type": artifact_type,
        "upgrade_level": upgrade_level,
        "upgraded_line": upgraded_line
    })
    st.success("Entry added!")

# Display
st.header("Upgrade Log")

if st.session_state.upgrade_log:
    df = pd.DataFrame(st.session_state.upgrade_log)
    st.dataframe(df, use_container_width=True)
else:
    st.write("No data logged yet.")