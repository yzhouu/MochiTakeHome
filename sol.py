import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
headers = ["Timestamp", "Mood", "Note"]
sheet = client.open("Mood Logger").sheet1

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

# UI design 
st.set_page_config(page_title="Mood Logger", page_icon="🧠", layout="centered")
st.title("🌞 Mood of the Queue 🌞")
st.subheader("How are you today my friend?")

st.markdown("-------")

col1, col2 = st.columns([1, 3])
with col1:
    mood = st.selectbox("Mood", list(moods.keys()))
with col2:
    note = st.text_input("Optional note")

if st.button("Submit Mood"):
    timestamp = datetime.now().isoformat()
    header_row = sheet.row_values(1)
    if header_row != headers:
        sheet.update('A1', [headers])
    sheet.append_row([timestamp, mood, note])
    st.success("✅ We got you!")

# Auto refresh
st_autorefresh(interval=60 * 1000, key="refresh")

# Load data
data = pd.DataFrame(sheet.get_all_records())

if not data.empty:
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    today = datetime.now().date()
    today_data = data[data['Timestamp'].dt.date == today]
    
    # Add a date filter
    all_dates = data['Timestamp'].dt.date.dropna().unique()
    all_dates = sorted(all_dates)

    selected_date = st.date_input("Select date to view moods", value=datetime.now().date(), min_value=min(all_dates), max_value=max(all_dates))

    # Filter data by selected date
    filtered = data[data['Timestamp'].dt.date == selected_date]

    # Grouping by mood
    mood_counts = today_data['Mood'].value_counts().reset_index()
    mood_counts.columns = ['Mood', 'Count']
    
    # Plot the bar chart
    fig = px.bar(mood_counts, x='Mood', y='Count', title='Today\'s Mood Count', labels={'Count': 'Number of Entries'})
    st.plotly_chart(fig)
else:
    st.info("No mood entries yet for today.")
