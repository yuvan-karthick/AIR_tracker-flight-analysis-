import streamlit as st
import queries as db

st.title("✈️ Flights")

st.subheader("Flights per Aircraft Model")
st.dataframe(db.flights_per_aircraft_model(), use_container_width=True)

st.subheader("Aircraft with > 5 Flights")
st.dataframe(db.aircraft_with_more_than_5_flights(), use_container_width=True)

st.subheader("Domestic vs International Flights")
st.dataframe(db.domestic_vs_international_flights(), use_container_width=True)

st.subheader("Recent Arrivals at DEL")
st.dataframe(db.recent_arrivals_at_del(), use_container_width=True)
