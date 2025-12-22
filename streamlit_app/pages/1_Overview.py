import streamlit as st
import queries as db

st.title("🏠 Overview")

st.metric("🛫 Total Airports", db.outbound_flights_by_airport().shape[0])
st.metric("✈️ Total Flights", db.flights_per_aircraft_model()["flight_count"].sum())
st.metric("🛩️ Total Aircraft Models", db.flights_per_aircraft_model().shape[0])
