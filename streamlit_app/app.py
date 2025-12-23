import streamlit as st

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

st.set_page_config(
    page_title="AirTracker",
    page_icon="✈️",
    layout="wide"
)
st.title("🛫 AirTracker Analytics Dashboard 🛬")


st.write(
    """
    This is the **AirTracker** analytics application.

    Use the **sidebar on the left** to navigate between pages:
    - Overview
    - Flights
    - Airports
    - Delays

    All data is fetched from a SQLite database and analyzed using SQL queries.
    """
)
