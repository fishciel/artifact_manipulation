import streamlit as st
import pandas as pd
import collections
from datetime import datetime

""" 
Basic setup:
    - title, headers, boxes
    - add entries
    - save entries
    - display current entries
"""

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

# Display entries
st.header("Upgrade Log")

if st.session_state.upgrade_log:
    df = pd.DataFrame(st.session_state.upgrade_log)
    st.dataframe(df, use_container_width=True)
else:
    st.write("No data logged yet.")

"""
Pattern Detection
"""

def get_upgrade_pairs(log):
    """
    Go through each entry and get the upgraded_line value (1-4)
    Convert to string and concat
    ex.
    ["1", "4", "4", "1", "2", "3"]
    ["14", "41", "23"], these pairs are returned
    """
    lines = [str(entry["upgraded_line"]) for entry in log]
    pairs = [lines[i] + lines[i+1] for i in range(len(lines) - 1)]
    return pairs

# Check for at least 2 upgrades (a pair)
if st.session_state.upgrade_log and len(st.session_state.upgrade_log) > 1:
    st.header("Upgrade patterns detected")

    # Display pairs and occurrences
    pairs = get_upgrade_pairs(st.session_state.upgrade_log)
    pair_counts = collections.Counter(pairs)

    df_pairs = pd.DataFrame(pair_counts.items(), columns=["Pattern", "Count"])
    df_pairs = df_pairs.sort_values(by="Count", ascending=False)

    st.table(df_pairs)
else:
    st.info("Add at least 2 upgrade events to analyze patterns.")

