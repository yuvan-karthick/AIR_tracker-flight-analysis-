import os
import json
import pandas as pd
from pandas import json_normalize
import sqlite3



DATA_DIR = "Flights_raw"

if not os.path.exists(DATA_DIR):
    print("Flights_raw folder not found")
    exit()



all_flight_records = []

for file in os.listdir(DATA_DIR):
    if not file.endswith(".json"):
        continue

    airport = file.split("_")[0]   # AMD_2025-... → AMD
    filepath = os.path.join(DATA_DIR, file)

    print(f"Loading cached file: {file}")

    with open(filepath, "r", encoding="utf-8") as f:
        records = json.load(f)

    all_flight_records.append((airport, records))

if not all_flight_records:
    print("No cached JSON files found")
    exit()



all_flight_records_flat = []

for origin_iata, item in all_flight_records:
    if isinstance(item, dict) and "departures" in item:
        for flight in item["departures"]:
            flight["origin_iata"] = origin_iata
            all_flight_records_flat.append(flight)

if not all_flight_records_flat:
    print(" No flight data after flattening")
    exit()

df = json_normalize(all_flight_records_flat, sep="_")



df_flights = pd.DataFrame()

df_flights["flight_number"] = df.get("number")
df_flights["aircraft_registration"] = df.get("aircraft_reg")
df_flights["origin_iata"] = df.get("origin_iata")
df_flights["destination_iata"] = df.get("arrival_airport_iata")

df_flights["scheduled_departure"] = df.get("departure_scheduledTime_utc")
df_flights["scheduled_arrival"] = df.get("arrival_scheduledTime_utc")

def pick_actual(a, r, v):
    return (
        df.get(a, pd.Series([None]*len(df)))
        .fillna(df.get(r, pd.Series([None]*len(df))))
        .fillna(df.get(v, pd.Series([None]*len(df))))
    )

df_flights["actual_departure"] = pick_actual(
    "departure_actualTime_utc",
    "departure_runwayTime_utc",
    "departure_revisedTime_utc"
)

df_flights["actual_arrival"] = pick_actual(
    "arrival_actualTime_utc",
    "arrival_runwayTime_utc",
    "arrival_revisedTime_utc"
)

df_flights["status"] = df.get("status")
df_flights["airline_code"] = df.get("airline_iata")

df_flights["flight_id"] = (
    df_flights["flight_number"].astype(str) + "_" +
    df_flights["scheduled_departure"].astype(str)
)

df_flights = df_flights[
    [
        "flight_id",
        "flight_number",
        "aircraft_registration",
        "origin_iata",
        "destination_iata",
        "scheduled_departure",
        "actual_departure",
        "scheduled_arrival",
        "actual_arrival",
        "status",
        "airline_code",
    ]
]

print("\nFinal FLIGHTS TABLE →")
print(df_flights.head(10).to_string(index=False))


conn = sqlite3.connect("airtracker.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS flights (
    flight_id TEXT PRIMARY KEY,
    flight_number TEXT,
    aircraft_registration TEXT,
    origin_iata TEXT,
    destination_iata TEXT,
    scheduled_departure TEXT,
    actual_departure TEXT,
    scheduled_arrival TEXT,
    actual_arrival TEXT,
    status TEXT,
    airline_code TEXT
);
""")

insert_sql = "INSERT OR IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?,?,?)"

for _, row in df_flights.iterrows():
    cur.execute(insert_sql, tuple(row))

conn.commit()
conn.close()
