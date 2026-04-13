import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, limit=None, key="refresh")

st.title("📊 Live Revenue Pulse Dashboard")

df = pd.read_csv("sales_data.csv")

# KPIs
total_revenue = df["Price"].sum()
orders = len(df)

col1, col2 = st.columns(2)

col1.metric("💰 Total Revenue", f"₹{total_revenue}")
col2.metric("📦 Orders", orders)

st.subheader("📍 Sales by City")
st.bar_chart(df.groupby("City")["Price"].sum())

st.subheader("🧾 Recent Sales")
st.dataframe(df.tail(10))

import requests

API_KEY = "f1bc9dda6a79f74641ec3383abd0b407"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    res = requests.get(url).json()
    
    weather = res["weather"][0]["main"]
    return weather
st.subheader("🌦️ Weather Impact")

cities = df["City"].unique()

for city in cities:
    weather = get_weather(city)
    
    if weather in ["Rain", "Thunderstorm"]:
        st.warning(f"{city}: 🌧️ Rain affecting sales")
    elif weather == "Clear":
        st.success(f"{city}: ☀️ Good sales conditions")
    else:
        st.info(f"{city}: {weather}")
        st.set_page_config(page_title="Revenue War Room", layout="wide")

st.markdown("## 🚨 Revenue Command Center")
st.markdown("---")