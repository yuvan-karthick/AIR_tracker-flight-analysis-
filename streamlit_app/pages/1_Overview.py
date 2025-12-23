import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE STYLES ----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 700;
        color: #2e7d32;
        text-align: center;
    }

    .hero-sub {
        text-align: center;
        font-size: 17px;
        color: #555;
        margin-bottom: 30px;
    }

    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
        text-align: center;
    }

    .kpi-label {
        font-size: 16px;
        color: #666;
    }

    .kpi-value {
        font-size: 38px;
        font-weight: 700;
        margin-top: 8px;
    }

    .green { color: #2e7d32; }
    .blue { color: #1f77b4; }
    .red { color: #c62828; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------
st.markdown("<div class='hero-title'>✈️ AirTracker Overview</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>High-level snapshot of airports, flights, and delay performance</div>",
    unsafe_allow_html=True
)

# ---------------- DB CONNECTION ----------------
conn = sqlite3.connect("../airtracker.db")

# ---------------- KPI QUERIES ----------------
total_airports = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM airport",
    conn
)["cnt"][0]

total_flights = pd.read_sql(
    "SELECT COUNT(*) AS cnt FROM flights",
    conn
)["cnt"][0]

avg_delay = pd.read_sql(
    """
    SELECT ROUND(
        100.0 * SUM(delayed_flights) / SUM(total_flights),
        2
    ) AS avg_delay
    FROM airport_delays
    WHERE total_flights > 0
    """,
    conn
)["avg_delay"][0]

total_aircraft_models = pd.read_sql(
    """
    SELECT COUNT(DISTINCT a.model) AS cnt
    FROM flights f
    JOIN aircrafts a
        ON f.aircraft_registration = a.registration
    WHERE a.model IS NOT NULL
    """,
    conn
)["cnt"][0]

# ✅ close connection ONCE, after all queries
conn.close()

# ---------------- KPI CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🛫 Total Airports</div>
            <div class="kpi-value blue">{total_airports}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">✈️ Total Flights</div>
            <div class="kpi-value green">{total_flights}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">⏱️ Avg Delay %</div>
            <div class="kpi-value red">{avg_delay}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🛩️ Total Aircraft Models</div>
            <div class="kpi-value blue">{total_aircraft_models}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
