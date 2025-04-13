# -*- coding: utf-8 -*-
"""aqi_to_gsheet.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kBXZgy42IfYYyWoM18OofYC3QvBFbC0D
"""

from google.colab import auth
import gspread
from google.auth import default
import random
import time
from datetime import datetime
import pytz

# Authenticate and create a client
auth.authenticate_user()
creds, _ = default()
client = gspread.authorize(creds)

# Open the spreadsheet (Replace with your Google Sheets ID)
sheet = client.open_by_key("1Owq1oL-Wh1kPliS3bzclm7W13tDYddJrxXjQzg6B3vs").sheet1

# If empty, add headers
if not sheet.get_all_values():
    sheet.append_row(["Location", "PM10", "PM2.5", "NO2", "SO2", "CO", "O3", "AQI", "AQI Category",
                      "Time", "Date", "Health Advisory"])

def generate_aqi_data(location, past_data):
    """Generates real-time AQI data based on past trends."""
    pm10 = max(0, random.uniform(past_data['PM10'] * 0.8, past_data['PM10'] * 1.2))
    pm25 = max(0, random.uniform(past_data['PM2.5'] * 0.8, past_data['PM2.5'] * 1.2))
    no2 = max(0, random.uniform(past_data['NO2'] * 0.8, past_data['NO2'] * 1.2))
    so2 = max(0, random.uniform(past_data['SO2'] * 0.8, past_data['SO2'] * 1.2))
    co = max(0, random.uniform(past_data['CO'] * 0.8, past_data['CO'] * 1.2))
    o3 = max(0, random.uniform(past_data['O3'] * 0.8, past_data['O3'] * 1.2))

    # Calculate AQI value (simplified)
    aqi = int(pm10 * 0.5 + pm25 * 0.4 + no2 * 20 + so2 * 15 + co * 5 + o3 * 10)

    # Categorize AQI
    if aqi <= 50:
        category, advisory = "Good", "Air quality is good. No precautions needed."
    elif aqi <= 100:
        category, advisory = "Moderate", "Air quality is acceptable. Sensitive groups should take precautions."
    elif aqi <= 150:
        category, advisory = "Poor", "People with respiratory issues should reduce outdoor activities."
    elif aqi <= 200:
        category, advisory = "Very Poor", "Limit outdoor exertion, especially children and elderly."
    else:
        category, advisory = "Hazardous", "Serious health effects. Avoid outdoor activities entirely."

    # Get current IST time
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    time_str = now.strftime('%H:%M:%S')  # Format: HH:MM:SS
    date_str = now.strftime('%Y-%m-%d')  # Format: YYYY-MM-DD

    return [location, round(pm10, 2), round(pm25, 2), round(no2, 4), round(so2, 4), round(co, 3),
            round(o3, 3), aqi, category, time_str, date_str, advisory]

# Example past AQI data for a city
past_aqi_data = {
    "PM10": 140,
    "PM2.5": 90,
    "NO2": 0.03,
    "SO2": 0.012,
    "CO": 1.0,
    "O3": 0.05
}

locations = [
    "Alipur", "Anand Vihar", "Ashok Vihar", "Dr. Karni Singh Shooting Range", "Dwarka, Sec-8", "Gurugram",
    "Jahangirpuri", "Jawaharlal Nehru Stadium", "Jorapokhar", "Major Dhyan Chand National Stadium", "Mandir Marg",
    "Mundka", "Najafgarh", "Narela", "Nehru Nagar", "Okhla Phase-2", "Patparganj", "Pooth Khurd, Bawana",
    "Punjabi Bagh", "Pusa", "R K Puram", "Rohini", "Sonia Vihar", "Sri Aurobindo Marg", "Supersite(Rouse Avenue)",
    "Vivek Vihar"
]

# Infinite loop to keep appending data every 2 seconds
while True:
    location = random.choice(locations)
    data = generate_aqi_data(location, past_aqi_data)
    sheet.append_row(data)  # Append new row in Google Sheets
    print("New AQI data added:", data)
    time.sleep(60)  # Wait for 60 seconds before generating new data