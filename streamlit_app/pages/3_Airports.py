import streamlit as st
import queries as db

st.title("🏢 Airports")

st.subheader("Outbound Flights by Airport")
st.dataframe(db.outbound_flights_by_airport(), use_container_width=True)

st.subheader("Top 3 Destination Airports")
st.dataframe(db.top_3_destination_airports(), use_container_width=True)

st.subheader("Airports with No Arrivals")
st.dataframe(db.airports_with_no_arrivals(), use_container_width=True)
