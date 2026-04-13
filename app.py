# ------------------ IMPORTS ------------------
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Revenue Command Center", layout="wide")

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=30000, key="auto_refresh")  # 30 sec refresh

# ------------------ LIVE DATA GENERATION ------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Time", "Product", "Price", "City"]
    )

products = ["Laptop", "Mobile", "Tablet", "Headphones", "Smartwatch"]
cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"]

# Add one new sale every refresh
new_row = {
    "Time": datetime.now(),
    "Product": random.choice(products),
    "Price": random.randint(1000, 50000),
    "City": random.choice(cities)
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
)

df = st.session_state.data
df["Time"] = pd.to_datetime(df["Time"])

# ------------------ TITLE ------------------
st.markdown("## 🚨 Revenue Command Center")
st.markdown("---")

# ------------------ KPIs ------------------
total_revenue = df["Price"].sum()
orders = len(df)
avg_order = round(df["Price"].mean(), 2)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"₹{total_revenue:,}")
col2.metric("📦 Orders", orders)
col3.metric("📊 Avg Order Value", f"₹{avg_order}")

st.markdown("---")

# ------------------ CHART 1 ------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("📍 Revenue by City")
    city_data = df.groupby("City")["Price"].sum()
    st.bar_chart(city_data)

# ------------------ CHART 2 ------------------
with col5:
    st.subheader("📦 Orders by Product")
    product_data = df["Product"].value_counts()
    st.bar_chart(product_data)

st.markdown("---")

# ------------------ CHART 3 ------------------
col6, col7 = st.columns(2)

with col6:
    st.subheader("📈 Revenue Over Time")
    time_data = df.groupby(df["Time"].dt.minute)["Price"].sum()
    st.line_chart(time_data)

# ------------------ CHART 4 ------------------
with col7:
    st.subheader("🏙️ Orders by City")
    city_orders = df["City"].value_counts()
    st.bar_chart(city_orders)

st.markdown("---")

# ------------------ CHART 5 ------------------
st.subheader("💸 Price Distribution")
st.area_chart(df["Price"])

st.markdown("---")

# ------------------ FILTER ------------------
st.subheader("🔍 Filter Data")

selected_city = st.selectbox("Select City", ["All"] + list(df["City"].unique()))

if selected_city != "All":
    df = df[df["City"] == selected_city]

# ------------------ TABLE ------------------
st.subheader("🧾 Recent Transactions")
st.dataframe(
    df.sort_values(by="Time", ascending=False).head(10),
    use_container_width=True
)