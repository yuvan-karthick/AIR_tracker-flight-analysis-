import sqlite3
import pandas as pd

DB_NAME = "airtracker.db"


# -------------------- CONNECTION HELPER --------------------
def get_connection():
    return sqlite3.connect(DB_NAME)


# -------------------- OVERVIEW METRICS --------------------
def total_airports():
    with get_connection() as conn:
        return pd.read_sql("SELECT COUNT(*) AS total FROM airport", conn)


def total_flights():
    with get_connection() as conn:
        return pd.read_sql("SELECT COUNT(*) AS total FROM flights", conn)


def total_aircrafts():
    with get_connection() as conn:
        return pd.read_sql("SELECT COUNT(*) AS total FROM aircrafts", conn)


def average_delay_percentage():
    query = """
    SELECT ROUND(
        100.0 * SUM(
            CASE 
                WHEN actual_arrival IS NOT NULL
                 AND scheduled_arrival IS NOT NULL
                 AND actual_arrival > scheduled_arrival
                THEN 1 ELSE 0
            END
        ) / COUNT(*), 2
    ) AS avg_delay
    FROM flights
    WHERE actual_arrival IS NOT NULL
      AND scheduled_arrival IS NOT NULL
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


# -------------------- FLIGHT ANALYTICS --------------------
def flights_per_aircraft_model():
    query = """
    SELECT a.model, COUNT(*) AS flight_count
    FROM flights f
    JOIN aircrafts a ON f.aircraft_registration = a.registration
    GROUP BY a.model
    ORDER BY flight_count DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def aircraft_with_more_than_5_flights():
    query = """
    SELECT a.registration, a.model, COUNT(*) AS flight_count
    FROM flights f
    JOIN aircrafts a ON f.aircraft_registration = a.registration
    GROUP BY a.registration, a.model
    HAVING COUNT(*) > 5
    ORDER BY flight_count DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def outbound_flights_by_airport():
    query = """
    SELECT ap.name AS airport_name, COUNT(*) AS outbound_flights
    FROM flights f
    JOIN airport ap ON f.origin_iata = ap.iata_code
    GROUP BY ap.name
    ORDER BY outbound_flights DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def top_3_destination_airports():
    query = """
    SELECT ap.name, ap.city, COUNT(*) AS arrivals
    FROM flights f
    JOIN airport ap ON f.destination_iata = ap.iata_code
    GROUP BY ap.name, ap.city
    ORDER BY arrivals DESC
    LIMIT 3
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def domestic_vs_international_flights():
    query = """
    SELECT 
        f.flight_number,
        o.country AS origin_country,
        d.country AS destination_country,
        CASE
            WHEN o.country = d.country THEN 'Domestic'
            ELSE 'International'
        END AS flight_type
    FROM flights f
    JOIN airport o ON f.origin_iata = o.iata_code
    JOIN airport d ON f.destination_iata = d.iata_code
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def recent_arrivals_at_del():
    query = """
    SELECT 
        f.flight_number,
        a.model AS aircraft,
        ap.name AS departure_airport,
        f.actual_arrival
    FROM flights f
    JOIN aircrafts a ON f.aircraft_registration = a.registration
    JOIN airport ap ON f.origin_iata = ap.iata_code
    WHERE f.destination_iata = 'DEL'
      AND f.actual_arrival IS NOT NULL
      AND f.actual_arrival != ''
    ORDER BY datetime(f.actual_arrival) DESC
    LIMIT 5
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def airports_with_no_arrivals():
    query = """
    SELECT ap.name, ap.city
    FROM airport ap
    LEFT JOIN flights f ON ap.iata_code = f.destination_iata
    WHERE f.destination_iata IS NULL
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def flight_status_by_airline():
    query = """
    SELECT 
        airline_code,
        SUM(
            CASE 
                WHEN actual_departure IS NOT NULL
                 AND scheduled_departure IS NOT NULL
                 AND actual_departure > scheduled_departure
                THEN 1 ELSE 0
            END
        ) AS delayed,
        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
        SUM(CASE WHEN status = 'On Time' THEN 1 ELSE 0 END) AS on_time
    FROM flights
    GROUP BY airline_code
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def cancelled_flights_details():
    query = """
    SELECT 
        f.flight_number,
        a.model AS aircraft,
        o.name AS origin_airport,
        d.name AS destination_airport,
        f.scheduled_departure
    FROM flights f
    JOIN aircrafts a ON f.aircraft_registration = a.registration
    JOIN airport o ON f.origin_iata = o.iata_code
    JOIN airport d ON f.destination_iata = d.iata_code
    WHERE f.status = 'Cancelled'
    ORDER BY f.scheduled_departure DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def city_pairs_multiple_aircraft_models():
    query = """
    SELECT 
        o.city AS origin_city,
        d.city AS destination_city,
        COUNT(DISTINCT a.model) AS aircraft_models
    FROM flights f
    JOIN aircrafts a ON f.aircraft_registration = a.registration
    JOIN airport o ON f.origin_iata = o.iata_code
    JOIN airport d ON f.destination_iata = d.iata_code
    GROUP BY origin_city, destination_city
    HAVING COUNT(DISTINCT a.model) > 2
    ORDER BY aircraft_models DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def delayed_percentage_by_destination():
    query = """
    SELECT 
        ap.name AS airport_name,
        ROUND(
            100.0 * SUM(
                CASE 
                    WHEN f.actual_arrival IS NOT NULL
                     AND f.scheduled_arrival IS NOT NULL
                     AND f.actual_arrival > f.scheduled_arrival
                    THEN 1 ELSE 0
                END
            ) / COUNT(*), 2
        ) AS delayed_percentage
    FROM flights f
    JOIN airport ap ON f.destination_iata = ap.iata_code
    GROUP BY ap.name
    ORDER BY delayed_percentage DESC
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)
