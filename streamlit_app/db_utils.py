import sqlite3

DB_NAME = "../airtracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME)
