AIR TRACKER – PROJECT OVERVIEW
● Project Purpose Air Tracker is an end-to-end aviation data analytics application built using real-world flight data. It collects data from external APIs, stores it in a structured SQLite database, performs analytical SQL queries, and visualizes insights through an interactive Streamlit dashboard.

● Core Functionalities ● Fetches airport, flight, aircraft, and delay data using REST APIs. ● Cleans and stores all data in a single, structured SQLite database. ● Performs complex analytical SQL queries to extract operational insights. ● Visualizes results through a modern, user-friendly Streamlit web application. ● Enables users to explore aviation data using custom filters and interactive dashboards.

● Technical Key Concepts ● REST API integration and response handling. ● API response caching to manage and stay within rate limits. ● Relational database design using SQLite. ● Advanced SQL including Joins, Aggregations, and CASE WHEN logic. ● Streamlit UI development with a clear separation of backend and frontend logic.

● Streamlit Application Features ● Homepage Dashboard: Displays total airports, flights fetched, and average delays. ● Flight Search: Search by flight number/airline with origin and date filters. ● Airport Viewer: Detailed location info, timezones, and inbound/outbound traffic logs. ● Delay Analysis: Statistical comparison of arrival versus departure delays. ● Route Insights: Identification of busiest routes and airline performance metrics.

● SQL Analysis & Logic ● Calculation of flight frequency per specific aircraft model. ● Identification of aircraft assigned to multiple flights. ● Classification of flights into Domestic vs. International categories. ● Analysis of cancellation rates and delay percentages by destination. ● Evaluation of route diversity across different aircraft models.

● Implementation Steps ● 1. Install dependencies via pip install -r requirements.txt. ● 2. Initialize the database by running the API scripts (Airport, Flight, Aircraft, Delay). ● 3. Launch the interactive dashboard using streamlit run streamlit_app/app.py.

● Technologies Used ● Python ● SQLite ● Pandas ● Streamlit ● REST APIs