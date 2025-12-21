import pandas as pd
import sqlite3

DB_NAME="airtracker.db"

def get_connection():
     return sqlite3.connect(DB_NAME)

conn= get_connection()

def get_total_airports():
     query= "SELECT COUNT(*) AS count FROM airport"
     with conn:
          return pd.read_sql(query,conn)["count"][0]
def get_total_aircrafts():
     query="SELECT COUNT (*) AS count FROM flights"
     with conn:
          return pd.read_sql(query,conn)["count"][0]      
     
def get_average_delay():
    query = """
        SELECT ROUND(AVG(avg_delay_min), 2) AS avg_delay
        FROM airport_delays
        WHERE avg_delay_min IS NOT NULL
    """
    with conn:
        result = pd.read_sql(query, conn)["avg_delay"][0]
        return result if result is not None else 0
def search_flights(flight_number=None, airline_code=None):
    query = """
        SELECT *
        FROM flights
        WHERE 1=1
    """
    params = []

    if flight_number:
        query += " AND flight_number LIKE ?"
        params.append(f"%{flight_number}%")

    if airline_code:
        query += " AND airline_code = ?"
        params.append(airline_code)

    with get_connection() as conn:
        return pd.read_sql(query, conn, params=params)


     
     