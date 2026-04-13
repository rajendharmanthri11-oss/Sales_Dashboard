# ------------------ IMPORTS ------------------
import streamlit as st
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Revenue Command Center", layout="wide")

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=30000, key="auto_refresh")  # 30 seconds

# ------------------ LIVE DATA GENERATION ------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Time", "Product", "Price", "City"]
    )

# Add one new sale every refresh
new_row = {
    "Time": datetime.now(),
    "Product": random.choice(["Laptop", "Mobile", "Tablet", "Headphones"]),
    "Price": random.randint(1000, 50000),
    "City": random.choice(["Mumbai", "Delhi", "Bangalore", "Hyderabad"])
}

st.session_state.data = pd.concat(
    [st.session_state.data, pd.DataFrame([new_row])],
    ignore_index=True
)

df = st.session_state.data

# ------------------ TITLE ------------------
st.markdown("## 🚨 Revenue Command Center")
st.markdown("---")

# ------------------ KPIs ------------------
total_revenue = df["Price"].sum()
orders = len(df)
avg_order = round(df["Price"].mean(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"₹{total_revenue:,}")
col2.metric("📦 Total Orders", orders)
col3.metric("📊 Avg Order Value", f"₹{avg_order}")

st.markdown("---")

# ------------------ CHARTS ------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("📍 Revenue by City")
    city_data = df.groupby("City")["Price"].sum()
    st.bar_chart(city_data)

with col5:
    st.subheader("📈 Revenue Over Time")
    df["Time"] = pd.to_datetime(df["Time"])
    time_data = df.groupby(df["Time"].dt.minute)["Price"].sum()
    st.line_chart(time_data)

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
st_autorefresh(interval=30000)