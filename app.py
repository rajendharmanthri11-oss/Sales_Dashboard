# ============================================================
#  REVENUE COMMAND CENTER  ·  Weather-Aware Sales Dashboard
#  Auto-refresh: 30s | Charts: 5 | Weather: OpenWeatherMap
# ============================================================
#
#  INSTALL:
#    pip install streamlit streamlit-autorefresh plotly pandas requests
#
#  RUN:
#    streamlit run revenue_command_center.py
# ============================================================

import random
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Revenue Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  AUTO REFRESH  (30 seconds)
# ──────────────────────────────────────────────
st_autorefresh(interval=30_000, key="dashboard_refresh")

# ──────────────────────────────────────────────
#  STYLES
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #080c14;
    --surface:   #0f1623;
    --surface2:  #151e2d;
    --border:    rgba(255,255,255,0.07);
    --cyan:      #00e5ff;
    --green:     #39ff7e;
    --amber:     #ffb300;
    --red:       #ff4560;
    --violet:    #b44eff;
    --text:      #e8edf7;
    --muted:     #6b7a99;
}

/* ── Base ── */
.stApp { background: var(--bg) !important; font-family: 'Outfit', sans-serif; }
.block-container { padding: 1.2rem 2rem 2rem !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #0b1020 !important; border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] * { color: var(--text) !important; }
header[data-testid="stHeader"] { background: transparent !important; }
footer { visibility: hidden; }

/* ── KPI Cards ── */
.kpi {
    background: linear-gradient(145deg, var(--surface), var(--surface2));
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-accent {
    position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 14px 14px 0 0;
}
.kpi-label {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem; color: var(--text); line-height: 1;
}
.kpi-sub { font-size: 0.75rem; color: var(--muted); margin-top: 5px; }
.kpi-badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.06em;
}
.up   { background: rgba(57,255,126,0.12); color: var(--green); }
.down { background: rgba(255,69,96,0.12);  color: var(--red); }
.neutral { background: rgba(0,229,255,0.1); color: var(--cyan); }

/* ── Weather Cards ── */
.wx-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.wx-city  { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); }
.wx-icon  { font-size: 1.8rem; line-height: 1.2; }
.wx-temp  { font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: var(--text); }
.wx-desc  { font-size: 0.68rem; color: var(--muted); margin-top: 2px; }
.wx-alert {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 2px 8px; border-radius: 8px; margin-top: 5px;
    display: inline-block;
}
.rain-alert  { background: rgba(0,229,255,0.15); color: var(--cyan); }
.heat-alert  { background: rgba(255,179,0,0.15);  color: var(--amber); }
.storm-alert { background: rgba(180,78,255,0.15); color: var(--violet); }
.clear-alert { background: rgba(57,255,126,0.12); color: var(--green); }

/* ── Section titles ── */
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem; letter-spacing: 0.1em;
    color: var(--text); margin: 1.4rem 0 0.6rem;
    display: flex; align-items: center; gap: 8px;
}
.sec-title::after { content:''; flex:1; height:1px; background: var(--border); }

/* ── Header ── */
.hdr { display:flex; align-items:flex-start; justify-content:space-between; padding-bottom: 1rem; border-bottom: 1px solid var(--border); margin-bottom: 1.2rem; }
.hdr-title { font-family:'Bebas Neue',sans-serif; font-size:2.2rem; color:var(--text); letter-spacing:0.06em; }
.hdr-title span { color: var(--cyan); }
.hdr-sub   { font-size:0.8rem; color:var(--muted); margin-top:2px; }
.live-pill {
    background: rgba(57,255,126,0.1); border: 1px solid var(--green);
    color: var(--green); font-size: 0.7rem; font-weight:700; letter-spacing:0.1em;
    padding: 4px 14px; border-radius: 20px; display:flex; align-items:center; gap:6px;
}
.pulse { width:7px; height:7px; background:var(--green); border-radius:50%;
    animation: blink 1.3s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.7)} }

/* ── Table ── */
[data-testid="stDataFrame"] { border-radius: 10px !important; border: 1px solid var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────
PRODUCTS = ["Laptop", "Mobile", "Tablet", "Headphones", "Smartwatch"]
CITIES   = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"]
COLORS   = ["#00e5ff", "#39ff7e", "#ffb300", "#ff4560", "#b44eff"]

CITY_COORDS = {
    "Mumbai":    (19.0760, 72.8777),
    "Delhi":     (28.6139, 77.2090),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai":   (13.0827, 80.2707),
}

# ──────────────────────────────────────────────
#  API KEY
# ──────────────────────────────────────────────
OWM_KEY   = "f1bc9dda6a79f74641ec3383abd0b407"
DEMO_MODE = False

# ──────────────────────────────────────────────
#  WEATHER FETCHER
# ──────────────────────────────────────────────
WEATHER_ICONS = {
    "Clear":        ("☀️",  "clear-alert",  "CLEAR"),
    "Clouds":       ("⛅",  "neutral",      "CLOUDY"),
    "Rain":         ("🌧️",  "rain-alert",   "RAIN ⚠"),
    "Drizzle":      ("🌦️",  "rain-alert",   "DRIZZLE"),
    "Thunderstorm": ("⛈️",  "storm-alert",  "STORM ⚠"),
    "Snow":         ("❄️",  "neutral",      "SNOW"),
    "Haze":         ("🌫️",  "neutral",      "HAZE"),
    "Mist":         ("🌫️",  "neutral",      "MIST"),
}

DEMO_WEATHER = {
    "Mumbai":    {"main": "Rain",   "desc": "moderate rain",   "temp": 29},
    "Delhi":     {"main": "Clear",  "desc": "clear sky",       "temp": 42},
    "Bangalore": {"main": "Clouds", "desc": "broken clouds",   "temp": 24},
    "Hyderabad": {"main": "Clear",  "desc": "sunny",           "temp": 38},
    "Chennai":   {"main": "Rain",   "desc": "heavy rain",      "temp": 31},
}

@st.cache_data(ttl=300)   # cache 5 min to avoid API hammering
def fetch_weather(city: str) -> dict:
    if DEMO_MODE:
        d = DEMO_WEATHER[city]
        return {"main": d["main"], "desc": d["desc"], "temp": d["temp"], "ok": True}
    lat, lon = CITY_COORDS[city]
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
    )
    try:
        r = requests.get(url, timeout=6)
        j = r.json()
        return {
            "main": j["weather"][0]["main"],
            "desc": j["weather"][0]["description"].title(),
            "temp": round(j["main"]["temp"]),
            "ok":   True,
        }
    except Exception:
        return {"main": "N/A", "desc": "Unavailable", "temp": "--", "ok": False}

def weather_sales_multiplier(main: str, temp: int) -> float:
    """
    Simulate weather impact:
      Rain/Storm  → fewer footfall → -15 to -25 %
      Heat (>38°) → fewer footfall → -10 %
      Clear/Cool  → normal / slight boost
    """
    if main in ("Rain", "Drizzle", "Thunderstorm"):
        return random.uniform(0.75, 0.88)
    if isinstance(temp, int) and temp >= 38:
        return random.uniform(0.88, 0.92)
    return random.uniform(0.97, 1.10)

# ──────────────────────────────────────────────
#  SALES DATA  (session state → grows each refresh)
# ──────────────────────────────────────────────
if "sales_df" not in st.session_state:
    # Seed with 40 historical rows so charts aren't empty on first load
    rows = []
    base_time = datetime.now()
    for i in range(40):
        city = random.choice(CITIES)
        rows.append({
            "Time":    base_time.replace(
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
            ),
            "Product": random.choice(PRODUCTS),
            "Price":   random.randint(1_000, 50_000),
            "City":    city,
        })
    st.session_state.sales_df = pd.DataFrame(rows)

# Fetch weather for each city
weather = {city: fetch_weather(city) for city in CITIES}

# Add new sale every refresh, price adjusted by weather multiplier
new_city  = random.choice(CITIES)
wx        = weather[new_city]
mult      = weather_sales_multiplier(wx["main"], wx.get("temp", 25))
new_price = int(random.randint(1_000, 50_000) * mult)

new_row = pd.DataFrame([{
    "Time":    datetime.now(),
    "Product": random.choice(PRODUCTS),
    "Price":   new_price,
    "City":    new_city,
}])
st.session_state.sales_df = pd.concat(
    [st.session_state.sales_df, new_row], ignore_index=True
)
df = st.session_state.sales_df.copy()
df["Time"] = pd.to_datetime(df["Time"])

# ──────────────────────────────────────────────
#  PLOTLY LAYOUT DEFAULTS
# ──────────────────────────────────────────────
def base_layout(**kwargs):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,22,35,0.7)",
        font=dict(family="Outfit, sans-serif", color="#6b7a99", size=11),
        title=dict(font=dict(family="Bebas Neue, sans-serif", color="#e8edf7", size=15)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        margin=dict(l=45, r=20, t=50, b=40),
        **kwargs,
    )

# ──────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Controls")
    st.markdown("---")
    sel_city = st.selectbox("Filter by City", ["All"] + CITIES)
    sel_prod = st.multiselect("Filter by Product", PRODUCTS, default=PRODUCTS)
    show_wx  = st.toggle("Show Weather Impact on Charts", value=True)
    st.markdown("---")
    st.success("🌐 Live Weather Connected")
    st.markdown("---")
    st.markdown("### 📍 Live Weather")
    for city in CITIES:
        wx = weather[city]
        main = wx["main"]
        icon, css, label = WEATHER_ICONS.get(main, ("🌡️","neutral", main.upper()))
        heat = isinstance(wx["temp"], int) and wx["temp"] >= 38
        badge_css  = "heat-alert" if heat and main == "Clear" else css
        badge_text = f"HEAT ⚠" if heat and main == "Clear" else label
        st.markdown(f"""
        <div class="wx-card" style="margin-bottom:8px">
            <div class="wx-city">{city}</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:8px">
                <span class="wx-icon">{icon}</span>
                <span class="wx-temp">{wx['temp']}°C</span>
            </div>
            <div class="wx-desc">{wx['desc']}</div>
            <span class="wx-alert {badge_css}">{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  FILTER DATA
# ──────────────────────────────────────────────
dff = df.copy()
if sel_city != "All":
    dff = dff[dff["City"] == sel_city]
dff = dff[dff["Product"].isin(sel_prod)]

# ──────────────────────────────────────────────
#  HEADER
# ──────────────────────────────────────────────
hcol1, hcol2 = st.columns([6, 1])
with hcol1:
    st.markdown(f"""
    <div class="hdr">
        <div>
            <div class="hdr-title">Revenue <span>Command</span> Center</div>
            <div class="hdr-sub">Weather-Aware · Real-time Sales Intelligence · {datetime.now().strftime('%A %d %B %Y  %H:%M:%S')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with hcol2:
    st.markdown('<div style="padding-top:12px;text-align:right"><div class="live-pill"><div class="pulse"></div>LIVE</div></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  KPI CARDS
# ──────────────────────────────────────────────
total_rev  = dff["Price"].sum()
orders_cnt = len(dff)
avg_order  = round(dff["Price"].mean(), 2) if orders_cnt else 0
top_city   = dff.groupby("City")["Price"].sum().idxmax() if orders_cnt else "—"
top_prod   = dff["Product"].value_counts().idxmax() if orders_cnt else "—"

# Weather alerts count
alert_cities = [c for c in CITIES if weather[c]["main"] in ("Rain","Drizzle","Thunderstorm")
                or (isinstance(weather[c]["temp"], int) and weather[c]["temp"] >= 38)]

kc = st.columns(5)

def kpi(col, label, val, sub, accent, badge="", badge_cls="neutral"):
    col.markdown(f"""
    <div class="kpi">
        <div class="kpi-accent" style="background:{accent}"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val}</div>
        <div class="kpi-sub">{sub}{"&nbsp;&nbsp;" if badge else ""}<span class="kpi-badge {badge_cls}">{badge}</span></div>
    </div>
    """, unsafe_allow_html=True)

kpi(kc[0], "Total Revenue",    f"₹{total_rev:,.0f}",    "Cumulative all products",     "#00e5ff", "▲ LIVE", "up")
kpi(kc[1], "Orders",           f"{orders_cnt:,}",        "Transactions recorded",       "#39ff7e", f"+1 now", "up")
kpi(kc[2], "Avg Order Value",  f"₹{avg_order:,.0f}",    "Per transaction",             "#ffb300")
kpi(kc[3], "Top City",         top_city,                 "Highest revenue city",        "#b44eff")
kpi(kc[4], "Weather Alerts",   f"{len(alert_cities)}",   "Cities affected",
    "#ff4560", "RAIN/HEAT" if alert_cities else "ALL CLEAR",
    "down" if alert_cities else "up")

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  CHART 1  —  Grouped Bar: Revenue by City + Weather overlay
# ──────────────────────────────────────────────
st.markdown('<div class="sec-title">🏙️ Revenue by City · Weather Impact</div>', unsafe_allow_html=True)

city_rev = dff.groupby("City")["Price"].sum().reindex(CITIES, fill_value=0)
wx_labels = []
bar_colors = []
for city in city_rev.index:
    wx_c = weather[city]
    main = wx_c["main"]
    temp = wx_c.get("temp", 25)
    if main in ("Rain", "Drizzle", "Thunderstorm"):
        wx_labels.append(f"🌧 {wx_c['desc']}")
        bar_colors.append("#00e5ff")
    elif isinstance(temp, int) and temp >= 38:
        wx_labels.append(f"🔥 {temp}°C Heat")
        bar_colors.append("#ffb300")
    else:
        wx_labels.append(f"✅ {wx_c['desc']}")
        bar_colors.append("#39ff7e")

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=list(city_rev.index),
    y=list(city_rev.values),
    marker_color=bar_colors if show_wx else COLORS,
    marker_line_width=0,
    text=[f"₹{v:,.0f}" for v in city_rev.values],
    textposition="outside",
    textfont=dict(color="#e8edf7", size=10),
    customdata=wx_labels,
    hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<br>Weather: %{customdata}<extra></extra>",
    name="Revenue",
))
if show_wx:
    # Overlay weather annotation bar
    for i, (city, lbl) in enumerate(zip(city_rev.index, wx_labels)):
        fig1.add_annotation(
            x=city, y=city_rev[city] * 0.05,
            text=lbl, showarrow=False,
            font=dict(size=9, color="#e8edf7"),
            bgcolor="rgba(0,0,0,0.4)",
            borderpad=3,
        )
fig1.update_layout(**base_layout(title="City Revenue — Color = Weather Condition", height=340))
st.plotly_chart(fig1, use_container_width=True)

# ──────────────────────────────────────────────
#  CHARTS 2 & 3
# ──────────────────────────────────────────────
c2, c3 = st.columns(2)

# CHART 2 — Donut: Orders by Product
with c2:
    st.markdown('<div class="sec-title">📦 Orders by Product</div>', unsafe_allow_html=True)
    prod_cnt = dff["Product"].value_counts()
    fig2 = go.Figure(go.Pie(
        labels=prod_cnt.index,
        values=prod_cnt.values,
        hole=0.6,
        marker=dict(colors=COLORS, line=dict(color="#080c14", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, family="Outfit, sans-serif"),
        pull=[0.05 if i == 0 else 0 for i in range(len(prod_cnt))],
    ))
    fig2.add_annotation(
        text=f"{prod_cnt.values.sum()}<br><span style='font-size:10px'>Orders</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="Bebas Neue, sans-serif", size=22, color="#e8edf7"),
        align="center",
    )
    fig2.update_layout(**base_layout(title="Product Order Distribution", height=340, showlegend=True,
        legend=dict(orientation="v", x=1.02, y=0.5)))
    st.plotly_chart(fig2, use_container_width=True)

# CHART 3 — Scatter: Price vs City colored by weather
with c3:
    st.markdown('<div class="sec-title">🌡️ Price Distribution · Weather Context</div>', unsafe_allow_html=True)

    def wx_color(city):
        wx_c = weather.get(city, {})
        main = wx_c.get("main", "Clear")
        temp = wx_c.get("temp", 25)
        if main in ("Rain", "Drizzle", "Thunderstorm"):
            return "Rain/Storm"
        if isinstance(temp, int) and temp >= 38:
            return "Heat Wave"
        return "Normal"

    dff_sc = dff.copy()
    dff_sc["WeatherType"] = dff_sc["City"].apply(wx_color)
    color_map = {"Rain/Storm": "#00e5ff", "Heat Wave": "#ffb300", "Normal": "#39ff7e"}

    fig3 = px.strip(
        dff_sc, x="City", y="Price", color="WeatherType",
        color_discrete_map=color_map,
        stripmode="overlay",
        hover_data={"Product": True, "Price": True, "WeatherType": True},
    )
    fig3.update_traces(marker=dict(size=7, opacity=0.75))
    fig3.update_layout(**base_layout(title="Transaction Prices by City — Weather Type", height=340))
    st.plotly_chart(fig3, use_container_width=True)

# ──────────────────────────────────────────────
#  CHARTS 4 & 5
# ──────────────────────────────────────────────
c4, c5 = st.columns(2)

# CHART 4 — Area: Revenue over time
with c4:
    st.markdown('<div class="sec-title">📈 Revenue Over Time</div>', unsafe_allow_html=True)
    time_df = (
        dff.set_index("Time")["Price"]
           .resample("1min").sum()
           .reset_index()
    )
    time_df.columns = ["Time", "Revenue"]
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=time_df["Time"], y=time_df["Revenue"],
        mode="lines",
        line=dict(color="#00e5ff", width=2),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.08)",
        name="Revenue",
        hovertemplate="<b>%{x|%H:%M}</b><br>₹%{y:,.0f}<extra></extra>",
    ))
    # Highlight alert cities on chart
    if show_wx and alert_cities:
        fig4.add_annotation(
            xref="paper", yref="paper", x=0.99, y=0.97,
            text="⚠️ " + ", ".join(alert_cities) + " weather alert",
            showarrow=False, font=dict(size=10, color="#ffb300"),
            bgcolor="rgba(255,179,0,0.1)", bordercolor="#ffb300",
            borderwidth=1, borderpad=4, align="right",
        )
    fig4.update_layout(**base_layout(title="Revenue Timeline (Per Minute)", height=320,
        xaxis=dict(title="Time", tickformat="%H:%M",
                   gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(255,255,255,0.08)")))
    st.plotly_chart(fig4, use_container_width=True)

# CHART 5 — Heatmap: Product × City
with c5:
    st.markdown('<div class="sec-title">🔥 Revenue Heatmap · Product × City</div>', unsafe_allow_html=True)
    heat_df = (
        dff.groupby(["City", "Product"])["Price"]
           .sum()
           .unstack(fill_value=0)
           .reindex(index=CITIES, columns=PRODUCTS, fill_value=0)
    )
    fig5 = go.Figure(go.Heatmap(
        z=heat_df.values,
        x=heat_df.columns.tolist(),
        y=heat_df.index.tolist(),
        colorscale=[
            [0.0,  "#0f1623"],
            [0.3,  "#004466"],
            [0.6,  "#007acc"],
            [0.85, "#00c8ff"],
            [1.0,  "#39ff7e"],
        ],
        text=[[f"₹{v:,.0f}" for v in row] for row in heat_df.values],
        texttemplate="%{text}",
        textfont=dict(size=9, color="#e8edf7"),
        hovertemplate="<b>%{y} · %{x}</b><br>₹%{z:,.0f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#6b7a99", size=9),
            outlinecolor="rgba(0,0,0,0)",
        ),
    ))
    # Mark affected cities
    if show_wx:
        for i, city in enumerate(heat_df.index):
            if city in alert_cities:
                wx_c  = weather[city]
                icon  = "🌧" if wx_c["main"] in ("Rain","Drizzle","Thunderstorm") else "🔥"
                fig5.add_annotation(
                    x=-0.9, y=i,
                    text=icon, showarrow=False,
                    font=dict(size=13),
                    xref="x", yref="y",
                )
    fig5.update_layout(**base_layout(title="Revenue Heatmap — City × Product", height=320))
    st.plotly_chart(fig5, use_container_width=True)

# ──────────────────────────────────────────────
#  WEATHER IMPACT SUMMARY BAR
# ──────────────────────────────────────────────
st.markdown('<div class="sec-title">🌦️ Weather Impact on Average Order Value</div>', unsafe_allow_html=True)

city_avg = dff.groupby("City")["Price"].mean().reindex(CITIES, fill_value=0)
wx_impact_colors = []
wx_impact_notes  = []
for city in city_avg.index:
    wx_c = weather[city]
    main = wx_c["main"]
    temp = wx_c.get("temp", 25)
    if main in ("Rain", "Drizzle", "Thunderstorm"):
        wx_impact_colors.append("#00e5ff")
        wx_impact_notes.append("🌧 Rain — lower AOV")
    elif isinstance(temp, int) and temp >= 38:
        wx_impact_colors.append("#ffb300")
        wx_impact_notes.append("🔥 Heat — lower AOV")
    else:
        wx_impact_colors.append("#39ff7e")
        wx_impact_notes.append("✅ Clear — normal AOV")

fig_wx = go.Figure(go.Bar(
    x=list(city_avg.index),
    y=list(city_avg.values),
    marker_color=wx_impact_colors,
    marker_line_width=0,
    text=[f"₹{v:,.0f}" for v in city_avg.values],
    textposition="outside",
    textfont=dict(color="#e8edf7", size=11),
    customdata=wx_impact_notes,
    hovertemplate="<b>%{x}</b><br>Avg Order: ₹%{y:,.0f}<br>%{customdata}<extra></extra>",
))
fig_wx.add_hline(
    y=city_avg.mean(), line_dash="dot", line_color="#ff4560", line_width=1.5,
    annotation_text=f"Overall Avg ₹{city_avg.mean():,.0f}",
    annotation_font=dict(color="#ff4560", size=10),
    annotation_position="top right",
)
fig_wx.update_layout(**base_layout(title="Avg Order Value per City  (🌧 Cyan = Rain · 🔥 Amber = Heat · ✅ Green = Clear)", height=300))
st.plotly_chart(fig_wx, use_container_width=True)

# ──────────────────────────────────────────────
#  RECENT TRANSACTIONS TABLE
# ──────────────────────────────────────────────
st.markdown('<div class="sec-title">🧾 Recent Transactions</div>', unsafe_allow_html=True)

df_table = dff.sort_values("Time", ascending=False).head(15).copy()
df_table["Weather"] = df_table["City"].apply(
    lambda c: f"{WEATHER_ICONS.get(weather[c]['main'], ('','',''))[0]} {weather[c]['desc']} ({weather[c]['temp']}°C)"
)
df_table["Time"] = df_table["Time"].dt.strftime("%H:%M:%S")
df_table["Price"] = df_table["Price"].apply(lambda x: f"₹{x:,}")
st.dataframe(df_table[["Time","Product","Price","City","Weather"]], use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
f1, f2, f3 = st.columns(3)
f1.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
f2.caption("🔄 Auto-refresh every 30 seconds via streamlit-autorefresh")
f3.caption("🌦️ Weather: OpenWeatherMap API  ·  Live")