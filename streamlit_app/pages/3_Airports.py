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

st.subheader("🛬 Outbound Flights by Airport")

df = db.outbound_flights_by_airport()
selected_airport = st.selectbox(
    "Select an airport",
    df["airport_name"].unique()
)
selected_df = df[df["airport_name"] == selected_airport]

st.markdown("### ✈️ Selected Airport Details")
st.dataframe(
    selected_df.reset_index(drop=True),
    use_container_width=True
)
import altair as alt

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("airport_name:N", sort="-y", title="Airport"),
        y=alt.Y("outbound_flights:Q", title="Outbound Flights"),
        color=alt.condition(
            alt.datum.airport_name == selected_airport,
            alt.value("#00FFFF"),      # CYAN for selected
            alt.value("#1f77b4")       # BLUE for others
        ),
        tooltip=["airport_name", "outbound_flights"]
    )
    .properties(height=500)
)

st.altair_chart(chart, use_container_width=True)


st.subheader("🌍 Top Destination Airports")

top_n = st.slider(
    "Select number of top destination airports",
    min_value=1,
    max_value=11,
    value=3
)

df = db.top_destination_airports(top_n)

st.dataframe(df.reset_index(drop=True), use_container_width=True)

import altair as alt

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("arrivals:Q", title="Number of Arrivals"),
        y=alt.Y("airport_name:N", sort="-x", title="Airport"),
        color=alt.value("#c13121"),
        tooltip=["airport_name", "city", "arrivals"]
    )
    .properties(height=200)
)

st.altair_chart(chart, use_container_width=True)


st.subheader("Airports with No Arrivals")
st.dataframe(db.airports_with_no_arrivals(), use_container_width=True)
