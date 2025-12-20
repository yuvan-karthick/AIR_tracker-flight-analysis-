import os
import json
import time
import sqlite3
import http.client
import pandas as pd

# =========================
# CONFIGURATION
# =========================

DB_NAME = "airtracker.db"
CACHE_DIR = "delay_raw"
RETRY_COUNT = 2

# 🔧 FIX 1: USE SAME START / END AS FLIGHTS (CRITICAL FIX)
START = "2025-10-13T00:00"
END   = "2025-10-13T05:00"

SAFE_START = START.replace(":", "-")
SAFE_END   = END.replace(":", "-")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# =========================
# SETUP: READ AIRPORTS FROM DB
# =========================

conn_db = sqlite3.connect(DB_NAME)
cur = conn_db.cursor()

cur.execute("""
    SELECT iata_code
    FROM airport
    WHERE iata_code IS NOT NULL AND iata_code != ""
""")

rows = cur.fetchall()
airports = [r[0].strip().upper() for r in rows]

print(f"Airports found for delay check: {len(airports)}")

if not airports:
    print("No airports found. Exiting.")
    conn_db.close()
    exit()

# =========================
# API SETUP
# =========================

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "fd10360abbmshe13e7d4676c8bd3p1493e1jsn7bef08ec1ad1",
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}

delay_records = []
USE_API = True   # 🔧 FIX 2: GLOBAL API KILL SWITCH (quota safety)

# =========================
# FETCH / LOAD DELAY DATA
# =========================

for airport in airports:

    filename = f"{CACHE_DIR}/{airport}_{SAFE_START}_{SAFE_END}.json"

    # ✅ CACHE FIRST (NO API HIT)
    if os.path.exists(filename):
        print(f"Loading cached delay data for {airport}")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        delay_records.append({"airport": airport, "data": data})
        continue

    # ⛔ API DISABLED → SKIP
    if not USE_API:
        print(f"API disabled. Skipping API for {airport}")
        continue

    print(f"Fetching delay data for {airport}")

    # 🔧 FIX 3: RANGE ENDPOINT (START → END)
    url = f"/airports/iata/{airport}/delays/{START}/{END}"

    for attempt in range(1, RETRY_COUNT + 1):
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        text = raw.decode("utf-8", errors="replace")

        print(f"Attempt {attempt}: HTTP {res.status}")

        if res.status == 200 and text.strip():
            data = json.loads(text)
            delay_records.append({"airport": airport, "data": data})

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            break

        if res.status == 429:
            print("QUOTA HIT — API DISABLED. USING CACHE ONLY.")
            USE_API = False   # 🔧 FIX 4: STOP ALL FUTURE API CALLS
            break

        time.sleep(0.5)

# =========================
# FLATTEN JSON → DATAFRAME
# =========================

if not delay_records:
    print("No delay data collected.")
    conn_db.close()
    exit()

rows = []

for item in delay_records:
    airport = item["airport"]
    data = item["data"]

    rows.append({
        "airport_iata": airport,
        "start_time": START,          # 🔧 FIX 5: STORE RANGE
        "end_time": END,
        "avg_departure_delay": data.get("departures", {}).get("averageDelay"),
        "avg_arrival_delay": data.get("arrivals", {}).get("averageDelay"),
        "delayed_departures": data.get("departures", {}).get("delayed"),
        "delayed_arrivals": data.get("arrivals", {}).get("delayed"),
    })

df_delays = pd.DataFrame(rows)

print("\nSample delay data →")
print(df_delays.head(10).to_string(index=False))

# =========================
# SQL: CREATE TABLE
# =========================

cur.execute("""
CREATE TABLE IF NOT EXISTS delays (
    delay_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_iata TEXT,
    start_time TEXT,
    end_time TEXT,
    avg_departure_delay INTEGER,
    avg_arrival_delay INTEGER,
    delayed_departures INTEGER,
    delayed_arrivals INTEGER
);
""")

conn_db.commit()

# =========================
# INSERT INTO SQL
# =========================

insert_sql = """
INSERT INTO delays (
    airport_iata,
    start_time,
    end_time,
    avg_departure_delay,
    avg_arrival_delay,
    delayed_departures,
    delayed_arrivals
) VALUES (?, ?, ?, ?, ?, ?, ?);
"""

for _, row in df_delays.iterrows():
    cur.execute(insert_sql, (
        row["airport_iata"],
        row["start_time"],
        row["end_time"],
        row["avg_departure_delay"],
        row["avg_arrival_delay"],
        row["delayed_departures"],
        row["delayed_arrivals"],
    ))

conn_db.commit()

# =========================
# VERIFY
# =========================

print("\nSample delays table →")
cur.execute("SELECT * FROM delays LIMIT 10;")
for r in cur.fetchall():
    print(r)

conn_db.close()
