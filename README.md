# Artifact RNG Pattern Tracker

A lightweight streamlit app to help log and analyze relic and artifact upgrade patterns in Genshin Impact and Honkai Star Rail.
-- Ultimately, to help uncover RNG behavior and upgrade trends through pattern detection.

## Features
- Log artifact upgrade events with:
    - Upgrade milestone (+3, +6, +9, +12, +15)
    - Upgrade substat line (1-4)
    - Initial number of substats
- View all logged upgrades in a clean table
- Detect raw upgrade patterns (ex. "14, "32")
- Detect normalized patterns using Caesar Shift
- Export Data as a CSV file

# Requirements
Python 3.8+
Install dependecies via:
pip install -r requirements.txt

requirements.txt
streamlit
pandas

# How to Run App
streamlit run app.py