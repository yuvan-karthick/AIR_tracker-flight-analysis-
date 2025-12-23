import streamlit as st
import queries as db

st.markdown(
    """
    <style>
    /* Page padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Section headers */
    h2 {
        color: #1f77b4;
    }

    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e1e4e8;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    "<h1 style='color:#2e7d32;'>🏠 Overview</h1>",
    unsafe_allow_html=True
)

st.metric("🛫 Total Airports", db.outbound_flights_by_airport().shape[0])
st.metric("✈️ Total Flights", db.flights_per_aircraft_model()["flight_count"].sum())
st.metric("🛩️ Total Aircraft Models", db.flights_per_aircraft_model().shape[0])
