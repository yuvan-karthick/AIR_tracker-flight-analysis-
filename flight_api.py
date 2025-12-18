import http.client 
import os
import json
import time
import pandas as pd
from pandas import json_normalize

AIRPORTS = ["LHR","JFK","DEL","BOM","BLR",
            "DXB","SIN","HYD","CCU","AMD","COK","PNQ"]

START = "2025-10-13T00:00"
END   = "2025-10-13T05:00"

SAFE_START = START.replace(":", "-")
SAFE_END = END.replace(":", "-")

RETRY_COUNT = 3

if not os.path.exists("aircraft_raw"):
    os.makedirs("aircraft_raw")

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "9dd7fc56a6msh464e7a794ef8e60p12bebbjsn49606a94a08d",
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}

all_flight_records = []

for airport in AIRPORTS:

    filename = f"aircraft_raw/{airport}_{SAFE_START}_{SAFE_END}.json"

    if os.path.exists(filename):
        print(f"Loading cached data for {airport}")
        with open(filename, "r", encoding="utf-8") as f:
            records = json.load(f)
        all_flight_records.append((airport, records))
        continue

    print(f"Fetching new data for {airport}")

    url = (
        f"/flights/airports/iata/{airport}/{START}/{END}"
        "?withLeg=true&direction=Both&withCancelled=true&withCodeshared=true"
        "&withCargo=true&withPrivate=true&withLocation=false"
    )

    for attempt in range(1, RETRY_COUNT+1):
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        text = raw.decode("utf-8", errors="replace")

        print(f"Attempt {attempt}: HTTP {res.status}")

        if res.status == 200 and text.strip():
            records = json.loads(text)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            all_flight_records.append((airport, records))
            print(f"Saved data for {airport}")
            break

        if attempt == RETRY_COUNT:
            print(f"Failed after {RETRY_COUNT} attempts for {airport}")

        time.sleep(0.5)

if not all_flight_records:
    print("There ain't no data available")
    exit()

all_flight_records_flat = []

for origin_iata, item in all_flight_records:
    if isinstance(item, dict) and "departures" in item:
        dep = item["departures"]
        if isinstance(dep, list):
            for flight in dep:
                flight["origin_iata"] = origin_iata
                all_flight_records_flat.append(flight)

if not all_flight_records_flat:
    print("No flight data available after flattening.")
    exit()

df = json_normalize(all_flight_records_flat, sep="_")

# --- BUILD FLIGHTS TABLE ---

df_flights = pd.DataFrame()

df_flights["flight_number"] = df.get("number")
df_flights["aircraft_registration"] = df.get("aircraft_reg")
df_flights["origin_iata"] = df.get("origin_iata")
df_flights["destination_iata"] = df.get("arrival_airport_iata")

df_flights["scheduled_departure"] = df.get("departure_scheduledTime_utc")
df_flights["scheduled_arrival"] = df.get("arrival_scheduledTime_utc")

def pick_actual(col_actual, col_runway, col_revised):
    actual = df.get(col_actual, pd.Series([None] * len(df)))
    runway = df.get(col_runway, pd.Series([None] * len(df)))
    revised = df.get(col_revised, pd.Series([None] * len(df)))
    return actual.fillna(runway).fillna(revised)

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
print(df_flights.head(20).to_string(index=False))


#SQL CONVERTION:::

import sqlite3

conn= sqlite3.connect("airtracker.db")
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights(
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
conn.commit()

insert_sql = """
INSERT OR IGNORE INTO flights (
    flight_id,
    flight_number,
    aircraft_registration,
    origin_iata,
    destination_iata,
    scheduled_departure,
    actual_departure,
    scheduled_arrival,
    actual_arrival,
    status,
    airline_code
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

for _, row in df_flights.iterrows():
    cursor.execute(insert_sql, tuple(row))
conn.commit()

cursor.execute("SELECT * from flights LIMIT 10 ")
rows= cursor.fetchall()

print("printing sample rows from flight →")
for r in rows:
    print(r)

conn.close()
