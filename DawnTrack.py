import requests
import streamlit as st
from datetime import datetime, timezone, timedelta

def get_coordinates(city_name):
    API_KEY = "4957901b5453a46183958e9be751a3d4"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200 or not data:
        st.error("Invalid response from the API or city not found.")
        return None
    return data[0]["name"]

def fetch_weather_data(city_name):
    API_KEY = "4957901b5453a46183958e9be751a3d4"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200:
        st.error("Invalid response from the API.")
        return None, None
    sunrise = data["sys"].get("sunrise")
    timezone_offset = data.get("timezone", 0)
    
    return sunrise, timezone_offset

def convert_utc_to_local(utc_timestamp, timezone_offset):
    utc_time = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime('%I:%M:%S %p')

st.title("Sunrise Time")
city = st.text_input("Enter city name")

if st.button("Get Sunrise Time"):
    if city:
        city_name = get_coordinates(city)
        if city_name:
            sunrise_time, timezone_offset = fetch_weather_data(city_name)
            if sunrise_time:
                formatted_time = convert_utc_to_local(sunrise_time, timezone_offset)
                st.subheader(f"Sunrise time in {city}: {formatted_time}")
            else:
                st.error("Could not fetch sunrise time. Please ")
        else:
            st.error("Invalid city name.")
    else:
        st.error("Please enter a valid city name.")
