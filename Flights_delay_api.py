import os
import json
import pandas as pd
import time
import http.client
import sqlite3
from pandas import json_normalize

DB_NAME = "airtracker.db"
CACHE_DIR = "delay_raw"
RETRY_COUNT = 2

START = "2025-10-13T00:00"
END   = "2025-10-13T05:00"

SAFE_START = START.replace(":", "-")
SAFE_END   = END.replace(":", "-")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

conn_db = sqlite3.connect(DB_NAME)
cur = conn_db.cursor()

cur.execute("""
SELECT iata_code FROM airport 
WHERE iata_code IS NOT NULL AND iata_code != ""
""")

rows = cur.fetchall()
airports = [r[0].strip().upper() for r in rows]

print("airports found for delay check:", len(airports))
if not airports:
    conn_db.close()
    exit()

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "fd10360abbmshe13e7d4676c8bd3p1493e1jsn7bef08ec1ad1",
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}

delay_records = []
USE_API = True

for airport in airports:
    filename = f"{CACHE_DIR}/{airport}_{SAFE_START}_{SAFE_END}.json"

    if os.path.exists(filename):
        print("loading the data for :", airport)
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        delay_records.append({"airport": airport, "data": data})
        continue

    if not USE_API:
        print("API disabled, skipping:", airport)
        continue

    # FIXED: delay API uses single timestamp, not START/END range
    url = f"/airports/iata/{airport}/delays/{START}"
    print("fetching delay data")

    for attempt in range(1, RETRY_COUNT + 1):
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        txt = raw.decode("utf-8", errors="replace")

        print(f"attempt for {airport} status is {res.status}")

        if res.status == 200 and txt.strip():
            data = json.loads(txt)
            delay_records.append({"airport": airport, "data": data})

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            break

        if res.status == 429:
            print("QUOTA HIT — API DISABLED. USING CACHE ONLY.")
            USE_API = False
            break

    time.sleep(0.5)

if not delay_records:
    conn_db.close()
    exit()   # FIXED: exit was missing parentheses

rows = []

for item in delay_records:
    airport = item["airport"]
    data = item["data"]

    rows.append({
    "airport_iata": airport,
    "start_time": START,
    "end_time": END,

    # Departures
    "dep_total_flights": data.get("departuresDelayInformation", {}).get("numTotal"),
    "dep_cancelled": data.get("departuresDelayInformation", {}).get("numCancelled"),
    "dep_median_delay": data.get("departuresDelayInformation", {}).get("medianDelay"),
    "dep_delay_index": data.get("departuresDelayInformation", {}).get("delayIndex"),

    # Arrivals
    "arr_total_flights": data.get("arrivalsDelayInformation", {}).get("numTotal"),
    "arr_cancelled": data.get("arrivalsDelayInformation", {}).get("numCancelled"),
    "arr_median_delay": data.get("arrivalsDelayInformation", {}).get("medianDelay"),
    "arr_delay_index": data.get("arrivalsDelayInformation", {}).get("delayIndex"),
})


df_delays = pd.DataFrame(rows)

print("sample 10 rows of df →")
print(df_delays.head(10).to_string(index=False))
