import streamlit as st
import sqlite3
import pandas as pd


st.set_page_config(
    page_title="AirTracker",
    page_icon="✈️",
    layout="wide"
)

st.title("AirTracker Analytics Dashboard 🌐")
st.write(
    "This dashboard shows flight, aircraft, airport, and delay analytics "
    "using data stored in a SQLite database."
)

DB_NAME = "airtracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME) 


conn = get_connection()

total_airports = pd.read_sql(
    "SELECT COUNT(*) AS count FROM airport",
    conn
)["count"][0]

total_flights = pd.read_sql(
    "SELECT COUNT(*) AS count FROM flights",
    conn
)["count"][0]

total_aircrafts = pd.read_sql(
    "SELECT COUNT(*) AS count FROM aircrafts",
    conn
)["count"][0]

conn.close()


col1, col2, col3 = st.columns(3)

col1.metric("🛫 Total Airports", total_airports)
col2.metric("🛩️ Total Flights", total_flights)
col3.metric(" Total Aircrafts", total_aircrafts)

st.subheader("📄 Sample Flights Data")

conn=get_connection()

df_flights=pd.read_sql(
    "SELECT * FROM flights LIMIT 10",
    conn
)

conn.close()
st.dataframe(df_flights)
