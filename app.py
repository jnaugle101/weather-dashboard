# app.py
import requests
from urllib.parse import quote
import pandas as pd
import streamlit as st

st.set_page_config(page_title="World Weather", page_icon="🌦️", layout="centered")

TZ_CITIES = [
    "America/New_York",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Europe/Moscow",
    "Asia/Shanghai",
    "Asia/Seoul",
    "Asia/Singapore",
    "Australia/Sydney",
]

def tz_to_city(tz: str) -> str:
    return tz.split("/")[-1].replace("_", " ")

@st.cache_data(ttl=300)  # cache for 5 min
def fetch_city_weather(city_name: str):
    city_q = quote(city_name)
    resp = requests.get(
        f"https://wttr.in/{city_q}",
        params={"format": "%t|%h|%w"},  # temp | humidity | wind
        timeout=10,
    )
    if not resp.ok:
        return {"Temperature": f"Error {resp.status_code}", "Humidity": "-", "Wind": "-"}
    parts = resp.text.strip().split("|")
    if len(parts) != 3:
        return {"Temperature": "Parse error", "Humidity": "-", "Wind": "-"}
    temp, humidity, wind = [p.strip() for p in parts]
    return {"Temperature": temp, "Humidity": humidity, "Wind": wind}

st.title("🌎 World Weather Dashboard")

rows = []
for tz in TZ_CITIES:
    city = tz_to_city(tz)
    data = fetch_city_weather(city)
    rows.append({"City": city, **data})

df = pd.DataFrame(rows, columns=["City", "Temperature", "Humidity", "Wind"])
st.dataframe(df, use_container_width=True)
st.caption("Data from wttr.in (no API key required). Updates every ~5 minutes.")
