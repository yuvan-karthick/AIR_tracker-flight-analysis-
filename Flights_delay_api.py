import os
import json
import pandas as pd
import time
import http.client
import sqlite3
from pandas import json_normalize

DB_NAME = "delay.db"
CACHE_DIR = "delay_raw"
RETRY_COUNT = 2

START="2025-10-13T00:00"
END="2025-10-13T05:00"

SAFE_START=START.replace(":","-")
SAFE_END=END.replace(":","-")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

conn_db=sqlite3.connect(DB_NAME)
cur=conn_db.cursor()

cur.execute("""
SELECT iata_code FROM airport WHERE iata_code IS NOT NULL AND iata_code !=""
""")

rows=cur.fetchall()
airports=[r[0].strip().upper() for r in rows]

print("airports found for delay check:",len(airports))
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
    filename=f"{DB_NAME}/{airport}_{SAFE_END}_{SAFE_END}.json"

    if os.path.exists(filename):
        print("loading the data for :",airport)
        with open(filename,"r",encoding="utf-8")as f:
            data=json.load(f)
        delay_records.append(f,)



