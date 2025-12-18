import os
import json
import pandas as pd
import time
import http.client
import sqlite3
from pandas import json_normalize

DB_NAME = "airtracker.db"
CACHE_DIR = "aircraft_raw"
RETRY_COUNT = 3

print("AIRCRAFT API DB PATH:", os.path.abspath(DB_NAME))

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# ---------------- LOAD DISTINCT REGISTRATIONS ----------------
conn_db = sqlite3.connect(DB_NAME)
cursor = conn_db.cursor()

cursor.execute("""
    SELECT DISTINCT aircraft_registration
    FROM flights
    WHERE aircraft_registration IS NOT NULL
      AND aircraft_registration != ""
""")

rows = cursor.fetchall()
registrations = [r[0].strip().upper() for r in rows]

print(f"Unique registrations found: {len(registrations)}")

if not registrations:
    print("No registrations found")
    conn_db.close()
    exit()

# ---------------- API CLIENT ----------------
conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "YOUR_KEY",
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}

USE_API = True
aircrafts_records = []

# ---------------- FETCH + CACHE LOOP ----------------
for reg in registrations:

    safe_reg = reg.replace("/", "-").replace(" ", "_")
    filename = f"{CACHE_DIR}/{safe_reg}.json"

    # ----- FIX 1: If API disabled, load only from cache -----
    if not USE_API:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                aircrafts_records.extend(data)
            else:
                aircrafts_records.append(data)
        continue

    # ----- Check cache first -----
    if os.path.exists(filename):
        print(f"Loading cached data for {reg}")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # FIX 3: Expand list into rows
        if isinstance(data, list):
            aircrafts_records.extend(data)
        else:
            aircrafts_records.append(data)

        continue

    print(f"Fetching data for {reg}")

    url = f"/aircrafts/reg/{reg}/all"

    for attempt in range(1, RETRY_COUNT + 1):
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        raw = res.read()
        text = raw.decode("utf-8", errors="replace")

        print(f"Attempt {attempt} → HTTP {res.status}")

        # API success
        if res.status == 200 and text.strip():
            try:
                data = json.loads(text)

                # FIX 4: Expand list safely
                if isinstance(data, list):
                    aircrafts_records.extend(data)
                else:
                    aircrafts_records.append(data)

                # Save cache
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                break

            except json.JSONDecodeError:
                print(f"JSON error for {reg}")

        # ----- FIX 5: Disable API on 429 -----
        if res.status == 429:
            print("QUOTA REACHED — API DISABLED. USING CACHE ONLY.")
            USE_API = False
            break

    time.sleep(0.3)

# ---------------- BUILD DATAFRAME ----------------
if not aircrafts_records:
    print("No aircraft data collected")
    conn_db.close()
    exit()

df = json_normalize(aircrafts_records)

# Manufacturer extraction helper
def get_manufacturer(type_name):
    if not isinstance(type_name, str):
        return None
    if "Airbus" in type_name:
        return "Airbus"
    if "Boeing" in type_name:
        return "Boeing"
    if "Embraer" in type_name:
        return "Embraer"
    return None

df_aircrafts = pd.DataFrame({
    "registration": df.get("reg"),
    "model": df.get("typeName"),               # FIX 6: correct model field
    "manufacturer": df["typeName"].apply(get_manufacturer),
    "icao_type_code": df.get("icaoCode"),
    "owner": df.get("airlineName").fillna("Unknown")
})

print("\nSample rows →")
print(df_aircrafts.head(10).to_string(index=False))

# ---------------- SAVE TO SQL ----------------
cur = conn_db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS aircrafts (
    aircraft_id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration TEXT UNIQUE,
    model TEXT,
    manufacturer TEXT,
    icao_type_code TEXT,
    owner TEXT
)
""")

insert_sql = """
INSERT OR IGNORE INTO aircrafts (
    registration, model, manufacturer, icao_type_code, owner
) VALUES (?, ?, ?, ?, ?)
"""
print("\nDATAFRAME CHECK BEFORE SQL INSERT")
print(df_aircrafts.head(5))
print(df_aircrafts.isna().sum())
print("Total rows:", len(df_aircrafts))

for _, row in df_aircrafts.iterrows():
    cur.execute(insert_sql, (
        row["registration"],
        row["model"],
        row["manufacturer"],
        row["icao_type_code"],
        row["owner"]
    ))

conn_db.commit()

print("\nSample aircrafts →")
cur.execute("SELECT * FROM aircrafts WHERE registration IS NOT NULL LIMIT 10 ")
rows = cur.fetchall()
for r in rows:
    print(r)

conn_db.close()
