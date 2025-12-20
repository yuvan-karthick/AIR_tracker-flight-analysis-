import os
import json
import time
import sqlite3
import http.client
import pandas as pd

DB_NAME = "airtracker.db"
CACHE_DIR = "delay_raw"
RETRY_COUNT = 2

START = "2025-10-13T00:00"
END   = "2025-10-13T05:00"
DELAY_DATE = START

SAFE_TIME = START.replace(":", "-")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

conn_db = sqlite3.connect(DB_NAME)
cur = conn_db.cursor()

cur.execute("""
SELECT iata_code FROM airport
WHERE iata_code IS NOT NULL AND iata_code != ""
""")

airports = [r[0].strip().upper() for r in cur.fetchall()]

print("airports found for delay check:", len(airports))
if not airports:
    conn_db.close()
    exit()

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "fd10360abbmshe13e7d4676c8bd3p1493e1jsn7bef08ec1ad1",
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}

delay_rows = []
USE_API = True

def time_to_minutes(t):
    if not t or not isinstance(t, str):
        return None
    h, m, s = t.split(":")
    return int(h) * 60 + int(m)

for airport in airports:
    filename = f"{CACHE_DIR}/{airport}_{SAFE_TIME}.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        if not USE_API:
            print("API disabled, skipping:", airport)
            continue

        url = f"/airports/iata/{airport}/delays/{START}"
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        txt = raw.decode("utf-8", errors="replace")

        print(f"{airport} → HTTP {res.status}")

        if res.status == 429:
            print("QUOTA HIT — API DISABLED")
            USE_API = False
            continue

        if res.status != 200 or not txt.strip():
            continue

        data = json.loads(txt)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    dep = data.get("departuresDelayInformation", {})
    arr = data.get("arrivalsDelayInformation", {})

    dep_total = dep.get("numTotal", 0) or 0
    arr_total = arr.get("numTotal", 0) or 0

    dep_cancel = dep.get("numCancelled", 0) or 0
    arr_cancel = arr.get("numCancelled", 0) or 0

    total_flights = dep_total + arr_total
    canceled_flights = dep_cancel + arr_cancel
    delayed_flights = total_flights - canceled_flights

    dep_median = time_to_minutes(dep.get("medianDelay"))
    arr_median = time_to_minutes(arr.get("medianDelay"))

    median_delay_min = None
    if dep_median is not None and arr_median is not None:
        median_delay_min = int((dep_median + arr_median) / 2)

    avg_delay_min = None
    dep_index = dep.get("delayIndex")
    arr_index = arr.get("delayIndex")
    if dep_index is not None and arr_index is not None:
        avg_delay_min = int(((dep_index + arr_index) / 2) * 10)

    delay_rows.append((
        airport,
        DELAY_DATE,
        total_flights,
        delayed_flights,
        avg_delay_min,
        median_delay_min,
        canceled_flights
    ))

cur.execute("""
CREATE TABLE IF NOT EXISTS airport_delays (
    delay_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_iata TEXT,
    delay_date TEXT,
    total_flights INTEGER,
    delayed_flights INTEGER,
    avg_delay_min INTEGER,
    median_delay_min INTEGER,
    canceled_flights INTEGER
);
""")

cur.executemany("""
INSERT INTO airport_delays (
    airport_iata,
    delay_date,
    total_flights,
    delayed_flights,
    avg_delay_min,
    median_delay_min,
    canceled_flights
) VALUES (?, ?, ?, ?, ?, ?, ?)
""", delay_rows)

conn_db.commit()

print("\nSample airport_delays →")
cur.execute("SELECT * FROM airport_delays LIMIT 10")
for r in cur.fetchall():
    print(r)

conn_db.close()
