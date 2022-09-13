import sqlite3 as sql
from os.path import exists

if exists("classes.db") == False:
    conn = sql.connect("classes.db")
    cur = conn.cursor()
    table = """ CREATE TABLE "Lessons"(
        unique_id INTEGER,
        less_name TEXT,
        less_number INTEGER,
        assignments TEXT,
        time TEXT,
        PRIMARY KEY(unique_id)
    )
    """
