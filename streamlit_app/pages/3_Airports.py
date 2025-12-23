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

#st.title("🏢 Airports")
st.markdown(
    "<h1 style='color:#1f77b4;'>🏢 Airports</h1>",
    unsafe_allow_html=True
)

st.subheader("Outbound Flights by Airport")
st.dataframe(db.outbound_flights_by_airport(), use_container_width=True)

st.subheader("Top 3 Destination Airports")
st.dataframe(db.top_3_destination_airports(), use_container_width=True)

st.subheader("Airports with No Arrivals")
st.dataframe(db.airports_with_no_arrivals(), use_container_width=True)
