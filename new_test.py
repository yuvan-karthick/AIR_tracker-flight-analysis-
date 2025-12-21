import streamlit as st
import test as db

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AirTracker Dashboard",
    page_icon="✈️",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("✈️ AirTracker Analytics Dashboard")
st.write(
    "This application analyzes flights, aircraft, airports, and delay data "
    "stored in a SQLite database."
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Navigation")

option = st.sidebar.selectbox(
    "Choose an analysis",
    [
        "Overview",
        "Flights per Aircraft Model",
        "Aircraft with > 5 Flights",
        "Outbound Flights by Airport",
        "Top Destination Airports",
        "Domestic vs International Flights",
        "Recent Arrivals at DEL",
        "Airports with No Arrivals",
        "Flight Status by Airline",
        "Cancelled Flights",
        "City Pairs with Multiple Aircraft Models",
        "Delayed Percentage by Airport"
    ]
)

# ---------------- MAIN CONTENT ----------------
if option == "Overview":
    st.subheader("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Airports", db.total_airports()["total"][0])
    col2.metric("Total Flights", db.total_flights()["total"][0])
    col3.metric("Total Aircrafts", db.total_aircrafts()["total"][0])
    col4.metric(
        "Avg Delay %",
        db.average_delay_percentage()["avg_delay"][0]
    )


elif option == "Flights per Aircraft Model":
    st.subheader("✈️ Flights per Aircraft Model")
    st.dataframe(db.flights_per_aircraft_model(), use_container_width=True)


elif option == "Aircraft with > 5 Flights":
    st.subheader("🛩️ Aircraft Assigned to More Than 5 Flights")
    st.dataframe(db.aircraft_with_more_than_5_flights(), use_container_width=True)


elif option == "Outbound Flights by Airport":
    st.subheader("🏢 Outbound Flights by Airport")
    st.dataframe(db.outbound_flights_by_airport(), use_container_width=True)


elif option == "Top Destination Airports":
    st.subheader("🌍 Top Destination Airports")
    st.dataframe(db.top_3_destination_airports(), use_container_width=True)


elif option == "Domestic vs International Flights":
    st.subheader("🏠 Domestic vs 🌍 International Flights")
    st.dataframe(db.domestic_vs_international_flights(), use_container_width=True)


elif option == "Recent Arrivals at DEL":
    st.subheader("🛬 Recent Arrivals at DEL Airport")
    st.dataframe(db.recent_arrivals_at_del(), use_container_width=True)


elif option == "Airports with No Arrivals":
    st.subheader("🚫 Airports with No Arriving Flights")
    st.dataframe(db.airports_with_no_arrivals(), use_container_width=True)


elif option == "Flight Status by Airline":
    st.subheader("📈 Flight Status Breakdown by Airline")
    st.dataframe(db.flight_status_by_airline(), use_container_width=True)


elif option == "Cancelled Flights":
    st.subheader("❌ Cancelled Flights Details")
    st.dataframe(db.cancelled_flights_details(), use_container_width=True)


elif option == "City Pairs with Multiple Aircraft Models":
    st.subheader("🔁 City Pairs with Multiple Aircraft Models")
    st.dataframe(db.city_pairs_multiple_aircraft_models(), use_container_width=True)


elif option == "Delayed Percentage by Airport":
    st.subheader("⏱️ Delayed Flights Percentage by Airport")
    st.dataframe(db.delayed_percentage_by_destination(), use_container_width=True)
