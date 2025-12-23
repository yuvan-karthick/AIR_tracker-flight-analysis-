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

#st.title("⏱️ Delays")
st.markdown(
    "<h1 style='color:#b71c1c;'>⏱️ Delays</h1>",
    unsafe_allow_html=True
)

st.subheader("Flight Status by Airline")
st.dataframe(db.flight_status_by_airline(), use_container_width=True)

st.subheader("Cancelled Flights")
st.dataframe(db.cancelled_flights_details(), use_container_width=True)
#st.write("Fortunately there were no")

st.subheader("City Pairs with Multiple Aircraft Models")
st.dataframe(db.city_pairs_multiple_aircraft_models(), use_container_width=True)

st.subheader("Delayed % by Airport")
st.dataframe(db.delayed_percentage_by_destination(), use_container_width=True)
