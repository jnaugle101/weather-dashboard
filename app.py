#live weather dashboard
import streamlit as st
import pandas as pd
import requests
import pytz
import requests
from urllib.parse import quote
from rich.console import Console
from rich.table import Table

console = Console()

tz_cities = [
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

table = Table(title="🌦️ Weather Dashboard", style="cyan", show_header=True, header_style="bold magenta")
table.add_column("City_Name", style="cyan", no_wrap=True)
table.add_column("Temperature", justify="center", style="magenta")
table.add_column("Humidity", justify="center", style="magenta")
table.add_column("Wind Speed", justify="center", style="magenta")

for tz in tz_cities:
    city = tz_to_city(tz)
    city_q = quote(city)
    try:
        resp = requests.get(f"https://wttr.in/{city_q}", params={"format": "%t|%h|%w"}, timeout=10)
        if resp.ok:
            parts = resp.text.strip().split("|")
            if len(parts) == 3:
                temp, humidity, wind = [p.strip() for p in parts]
                table.add_row(city, temp, humidity, wind)

            else:
                table.add_row(city, f"Error {resp.status_code}", "", "")

    except Exception as e:
        table.add_row(city, f"Exception {e.__class__.__name__}", "", "")



console.print(table)
