#live weather dashboard
import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
#from rich.console import Console
#from rich.table import Table

st.set_page_config(page_title="World Weather", page_icon="🌦️", layout="centered")
st.title("🌎 World Weather Dashboard")

TZ_CITIES = [
    "America/New_York",
    "America/Chicago",
    "America/Detroit",
    "America/Phoenix",
    "America/Los_Angeles",
    "America/Anchorage",
    "America/Denver",
    "America/Boise",
    "America/Phoenix",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Europe/Moscow",
    "Asia/Shanghai",
    "Asia/Seoul",
    "Asia/Singapore",
    "Australia/Sydney",
    "Europe/Berlin",
    "Europe/Rome",
    "Europe/Milan",
    "Europe/Warsaw",
    "Europe/Lisbon",
    "Europe/Madrid",
    "Europe/Stockholm",
    "Europe/Oslo",
    "Europe/Helsinki",
    "Europe/Copenhagen",
    "Europe/London",
]

def tz_to_city(tz: str) -> str:
    return tz.split("/")[-1].replace("_", " ")

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; StreamlitRender/1.0)"})

@st.cache_data(ttl=300)
def fetch_city_weather(city_name: str):
    try:
        city_q = quote(city_name)
        r = session.get(f"https://wttr.in/{city_q}", params={"format": "j1"}, timeout=8)
        if not r.ok:
            return {"Temperature": f"Error {r.status_code}", "Humidity": "-", "Wind": "-"}
        j = r.json()
        cur = (j.get("current_condition") or [{}])[0]
        # choose °F or °C; here we show °F (swap to temp_C if you prefer)
        temp = cur.get("temp_F")
        hum = cur.get("humidity")
        wind = cur.get("windspeedMiles")
        return {
            "Temperature": f"{temp}°F" if temp is not None else "-",
            "Humidity": f"{hum}%" if hum is not None else "-",
            "Wind": f"{wind} mph" if wind is not None else "-",
        }
    except Exception as e:
        return {"Temperature": f"Exception: {e.__class__.__name__}", "Humidity": "-", "Wind": "-"}

with st.status("Fetching weather…", expanded=False):
    rows = []
    for tz in TZ_CITIES:
        city = tz_to_city(tz)
        data = fetch_city_weather(city)
        rows.append({"City": city, **data})

df = pd.DataFrame(rows, columns=["City", "Temperature", "Humidity", "Wind"])
st.dataframe(df, use_container_width=True)
st.caption("Data from wttr.in (no API key required). Updates every ~5 minutes.")