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

#st.title("✈️ Flights")
st.markdown(
    "<h1 style='color:#1f77b4;'>✈️ Flights</h1>",
    unsafe_allow_html=True
)
st.subheader("Flights per Aircraft Model")
st.dataframe(db.flights_per_aircraft_model(), use_container_width=True)

st.subheader("Aircraft with > 5 Flights")
st.dataframe(db.aircraft_with_more_than_5_flights(), use_container_width=True)

st.subheader("Domestic vs International Flights")
st.dataframe(db.domestic_vs_international_flights(), use_container_width=True)

st.subheader("Recent Arrivals at DEL")
st.dataframe(db.recent_arrivals_at_del(), use_container_width=True)
