import streamlit as st
import queries as db

st.title("⏱️ Delays")

st.subheader("Flight Status by Airline")
st.dataframe(db.flight_status_by_airline(), use_container_width=True)

st.subheader("Cancelled Flights")
st.dataframe(db.cancelled_flights_details(), use_container_width=True)

st.subheader("City Pairs with Multiple Aircraft Models")
st.dataframe(db.city_pairs_multiple_aircraft_models(), use_container_width=True)

st.subheader("Delayed % by Airport")
st.dataframe(db.delayed_percentage_by_destination(), use_container_width=True)
