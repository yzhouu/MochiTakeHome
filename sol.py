import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from streamlit_gsheets import GSheetsConnection

# Page config
st.set_page_config(page_title="Mood Logger", page_icon="🧠", layout="centered")
st.title("🌞 Mood of the Queue 🌞")
st.subheader("How are you today my friend?")
st.markdown("-------")

# Create a GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the sheet as DataFrame
data = conn.read()

# Define expected columns
headers = ["Timestamp", "Mood", "Note"]

# Mood options
moods = {
    "😊": "Joy",
    "😠": "Mad",
    "😕": "Little Unhappy",
    "🎉": "Celebrate!",
    "😑": "Nothing to share",
    "☺️": "A little happy",
    "👽": "You tell me"
}

# UI for mood input
col1, col2 = st.columns([1, 3])
with col1:
    mood = st.selectbox("Mood", list(moods.keys()))
with col2:
    note = st.text_input("Optional note")

# Handle submission
if st.button("Submit Mood"):
    timestamp = datetime.now().isoformat()
    new_row = pd.DataFrame([[timestamp, mood, note]], columns=headers)

    # Write to the sheet by appending
    conn.update(data=pd.concat([data, new_row], ignore_index=True))
    st.success("✅ We got you!")

# Auto refresh
st_autorefresh(interval=60 * 1000, key="refresh")

# If sheet has any data
if not data.empty:
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    all_dates = data['Timestamp'].dt.date.dropna().unique()
    all_dates = sorted(all_dates)

    today = datetime.now().date()
    selected_date = st.date_input("Select date to view moods", value=today, min_value=min(all_dates), max_value=max(all_dates))
    
    # Filter for selected day
    filtered = data[data['Timestamp'].dt.date == selected_date]

    if not filtered.empty:
        mood_counts = filtered['Mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']

        fig = px.bar(mood_counts, x='Mood', y='Count', title='Mood Count', labels={'Count': 'Number of Entries'})
        st.plotly_chart(fig)
    else:
        st.info("No mood entries yet for this day.")
else:
    st.info("No mood entries yet.")
