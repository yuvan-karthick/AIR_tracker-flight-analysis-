import streamlit as st

st.set_page_config(
    page_title="AirTracker",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AirTracker Analytics Dashboard")

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
