import http.client
import pandas as pd
import os
import json
import time
import sqlite3
from pandas import json_normalize

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    "x-rapidapi-key": "API KEY",
    "x-rapidapi-host": "API HOST"
}

CODES = ["LHR","JFK","CBJ","DEL","BOM","BLR","DXB","SIN","HYD","CCU","AMD","COK","GOX","PNQ"]
cache = "airport_raw.json"

airport_list = []

if os.path.exists(cache):
    with open(cache, "r", encoding="utf-8") as f:
        airport_list = json.load(f)
    print(f"Loaded {len(airport_list)} records from cache '{cache}'")

    cached_iatas = {a.get("iata") for a in airport_list if isinstance(a, dict) and a.get("iata")}
    cached_iatas = {code.strip().upper() for code in cached_iatas if code}
    missing_codes = [code for code in CODES if code not in cached_iatas]

    if not missing_codes:
        print("All requested IATA codes already cached — skipping API calls.")
    else:
        print(f"Missing {len(missing_codes)} codes: {missing_codes} — fetching those now.")
else:
    missing_codes = CODES.copy()
    print("No cache found — fetching all codes from API...")

if missing_codes:
    for code in missing_codes:
        conn.request("GET", f"/airports/iata/{code}", headers=headers)
        res = conn.getresponse()
        raw_bytes = res.read()
        status = res.status
        text = raw_bytes.decode("utf-8", errors="replace")

        print(f"[{code}] HTTP {status} {res.reason} — {len(text)} bytes")

        if status == 204 or not text.strip():
            print(f"  → No content for {code} — skipping")
            time.sleep(0.12)
            continue

        if status != 200:
            print(f"  → Non-200 status for {code}: {status} {res.reason} — skipping")
            time.sleep(0.2)
            continue

        try:
            airport = json.loads(text)
        except json.JSONDecodeError as e:
            with open(f"debug_{code}.txt", "w", encoding="utf-8") as dbg:
                dbg.write(text)
            print(f"  → JSON decode failed for {code}: {e}")
            time.sleep(0.12)
            continue

        if isinstance(airport, dict) and ("iata" in airport or "icao" in airport):
            airport_list.append(airport)
            print(f"  → Appended {code}")
        else:
            print(f"  → Unexpected payload for {code} — skipping")

        time.sleep(0.12)

    with open(cache, "w", encoding="utf-8") as f:
        json.dump(airport_list, f, indent=2, ensure_ascii=False)
    print(f"Saved/updated cache with {len(airport_list)} records to '{cache}'")

if not airport_list:
    raise RuntimeError("No valid airport records available.")

df = json_normalize(airport_list, sep="_")

#print("\nSample columns (first 40):")
#print(df.columns.tolist()[:40])
#print("\nFirst row (transposed) preview:")
#print(df.head(1).T)

rename_map = {
    "location_lat": "lat",
    "location_lon": "lon",
    "elevation_meter": "elevation_m",
    "shortName": "short_name",
    "fullName": "full_name",
    "municipalityName": "city",
    "country_name": "country_name",
    "timeZone": "timezone"
}

existing = {k: v for k, v in rename_map.items() if k in df.columns}
df = df.rename(columns=existing)

wanted = [c for c in [
    "iata","icao","short_name","full_name","city","lat","lon",
    "elevation_m","country_name","timezone","continent_name"
] if c in df.columns]
df = df[wanted]

#print("\nRenamed & filtered DataFrame preview:")
#print(df.head(3).to_string(index=False))

df_sql = df.rename(columns={
    "icao": "icao_code",
    "iata": "iata_code",
    "full_name": "name",
    "city": "city",
    "country_name": "country",
    "continent_name": "continent",
    "lat": "latitude",
    "lon": "longitude",
    "timezone": "timezone"
})

cols = ["icao_code","iata_code","name","city","country","continent","latitude","longitude","timezone"]
df_sql = df_sql[[c for c in cols if c in df_sql.columns]]

#print("\nPrepared df_sql columns:", df_sql.columns.tolist())
print("\nFinal df_sql sample:")
print(df_sql.head(10).to_string(index=False))

#SQL CONVERTION:::
db_file="airtracker.db"
conn_db= sqlite3.connect(db_file)
cur = conn_db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS airport ( 
        airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
        icao_code TEXT UNIQUE,
        iata_code TEXT UNIQUE,
        name TEXT,
        city TEXT,
        country TEXT,
        continent TEXT,
        latitude REAL,
        longitude REAL,
        timezone TEXT
            )
""")

insert_sql="""
INSERT OR IGNORE INTO airport
(icao_code,iata_code,name,city,country,continent,latitude,longitude,timezone)
values(?,?,?,?,?,?,?,?,?)
            """
for rows in df_sql.itertuples(index=False,name=None):
    cur.execute(insert_sql,rows)

conn_db.commit()

