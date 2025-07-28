import streamlit as st
import pandas as pd
import collections
from datetime import datetime

#----------- Basic setup: -------------
#    - title, headers, boxes
#    - add entries
#    - save entries
#    - display current entries

# Name/title
st.title("Artifact RNG Pattern Tracker")
# Captions
st.caption("Primarily for Genshin Impact and Honkai Star Rail patterns")
st.caption("HSR lvls: +3, +6, +9, +12, +15")
st.caption("Genshin equivalent: +4, +8, +12, +16, +20")

st.header("Log a new upgrade event")

with st.form("upgrade_form"):
    # Artifact substats may have 0-4 lines depending on it's rarity
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

    # ---------- Let users download upgrade log
    # Download button for log only
    st.subheader("Download Upgrade Log Only")
    timestamp_str = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    file_name = f"{timestamp_str}_upgrade_log.csv"
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Upgrade Log as CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )
else:
    st.write("No data logged yet.")

# ---------- Pattern Detection ------------

# Raw pattern
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

# Normalized pattern
def normalize_pair(pair):
    """
    Normalize the pair using Caesar shift
    1234123412341234
    ex.   12, 23, 34, 41 => Cycle+1
          13, 24, 31, 42 => Cycle+2
          11, 22, 33, 44 => Cycle+0 (same line)

    i.e. if the shifts are the same movement then it is the same pattern 
    regardless of the upgraded lines
    """

    a, b = int(pair[0]), int(pair[1])
    # Check the shift
    diff = (b - a) % 4
    return f"Shift+{diff}"

# New df box for pattern detection
# Check for at least 2 upgrades (1 pair)
if st.session_state.upgrade_log and len(st.session_state.upgrade_log) > 1:
    st.header("Upgrade patterns detected")

    # RAW pairs and occurrences
    pairs = get_upgrade_pairs(st.session_state.upgrade_log)
    pair_counts = collections.Counter(pairs)
    df_pairs = pd.DataFrame(pair_counts.items(), columns=["Raw Pattern", "Count"])
    df_pairs = df_pairs.sort_values(by="Count", ascending=False)
    # Table w/raw pairs
    st.subheader("Raw Upgrade Pairs")
    st.table(df_pairs)

    # NORMALIZED (shift/cycle based)
    normalized = [normalize_pair(p) for p in pairs]
    normalized_counts = collections.Counter(normalized)
    df_normalized = pd.DataFrame(normalized_counts.items(), columns=["Pattern Group", "Count"])
    df_normalized = df_normalized.sort_values(by="Count", ascending=False)
    # Table w/normalized pattern groups
    st.subheader("Normalized Pattern Groups (Caesar Shift)")
    df_normalized = pd.DataFrame(normalized_counts.items(), columns=["Shift Pattern", "Count"])
    st.table(normalized)

    # ----------- Let users save/download their data
    st.subheader("Download PATTERN data as CSV")

    # Combine all tables into one df
    all_data_df = pd.concat([df_pairs, df_normalized], ignore_index=True)
    # Filename
    timestamp_str = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    file_name = f"{timestamp_str}_artifact_upgrade_data.csv"

    # CSV file
    csv = all_data_df.to_csv(index=False)
    st.download_button(
        label="Download All Data as CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )

else:
    st.info("Add at least 2 upgrade events to analyze patterns.")

