✈️ Air Tracker – Flight Analysis Project

This project is an end-to-end aviation data analysis application built using real flight data. It collects information from APIs, stores it in a SQLite database, and visualizes insights through a Streamlit web application.

The goal of this project is to analyze flights, aircraft, airports, and delays, and present meaningful insights in an easy-to-understand dashboard.

📌 What This Project Does

Fetches airport, flight, aircraft, and delay data using APIs

Stores all cleaned data in a single SQLite database

Performs analytical SQL queries on the data

Displays results in a modern Streamlit dashboard

Allows users to explore flights, delays, routes, and airport statistics

🗂️ Project Structure
02-air_tracker_project/
│
├── airtracker.db
│
├── airport_api.py          # Fetches and stores airport data
├── flight_api.py           # Fetches and stores flight data
├── aircraft_api.py         # Fetches and stores aircraft data
├── Flights_delay_api.py    # Fetches and stores delay statistics
│
├── streamlit_app/
│   ├── app.py              # Main Streamlit application
│   ├── db_utils.py         # Database helper & query functions
│   ├── queries.py          # All SQL queries used by the app
│
├── delay_raw/              # Cached delay API responses
├── aircraft_raw/           # Cached aircraft API responses
│
├── requirements.txt
└── README.md

🧠 Key Concepts Used

REST API integration

Data caching to avoid API quota issues

SQLite database design

SQL joins, aggregations, and case statements

Streamlit UI development

Clean separation of backend logic and frontend UI

📊 Features in the Streamlit App
Homepage Dashboard

Total number of airports

Total flights fetched

Average delays across airports

Flight Search & Filters

Search flights by number or airline

Filter by origin, destination, status, or date

Airport Details Viewer

Airport information

Linked inbound and outbound flights

Delay Analysis

Delay statistics by airport

Comparison between arrival and departure delays

Route & Airline Insights

Busiest routes

Most delayed airports

Flight status breakdown by airline

🧪 SQL Analysis Covered

This project answers analytical questions such as:

Flights per aircraft model

Aircraft used in multiple flights

Airports with high traffic

Domestic vs international flights

Delay percentages by airport

Cancelled flights analysis

Route diversity by aircraft models

(All queries are handled in queries.py and executed via Streamlit.)

▶️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Make sure database exists

Run the API scripts in this order (only once):

python airport_api.py
python flight_api.py
python aircraft_api.py
python Flights_delay_api.py

3️⃣ Run Streamlit app
streamlit run streamlit_app/app.py

🛠️ Technologies Used

Python

SQLite

Pandas

Streamlit

REST APIs

🎯 Outcome

This project demonstrates the complete workflow of:

Collecting real-world data

Designing a database

Writing analytical SQL queries

Building an interactive dashboard

It strengthens skills in data engineering, SQL, Python, and frontend visualization.

📌 Notes

API responses are cached locally to prevent repeated API calls

The database is read-only in Streamlit to ensure data safety

The project is modular and easy to extend

👨‍💻 Author

Yuvan Karthick
Aspiring Data Engineer / ML Engineer
Project built as part of advanced API, SQL & analytics learning


-------------------------------------------------------------------

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
