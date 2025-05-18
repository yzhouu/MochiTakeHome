# The Mood Logger 🌞

This is a real-time mood tracking application built with Streamlit that allows users to log and visualize their moods throughout the day. The application stores data in Google Sheets and provides interactive visualizations and filter based on day.
This Logger is intergrated in Streamlit.io. 

## What is required to run the project

- Need to install Python 3.7+
- Need to have Google Cloud Platform account with Google Sheets API enabled
- Need to have Google service account credentials

## Steps for Installation

1. First, clone the repository:
```bash
git clone https://github.com/yourusername/MoodLogger.git
cd MoodLogger
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Sheets credentials:
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create a service account and download the credentials
   - Add the credentials to Streamlit secrets, do not push to git


## How to use the page

1. Select current mood from the dropdown menu
2. Add an optional note if user want
3. Click "Submit Mood" to log the entry
4. View the mood distribution chart for the current day
5. Use the date picker to view moods from different days

## Dependencies

- streamlit
- gspread
- oauth2client
- pandas
- plotly
- streamlit-autorefresh