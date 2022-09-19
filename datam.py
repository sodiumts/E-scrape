import sqlite3 as sql
from os.path import exists



def manager():
    
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

        cur.execute(table)

    with sql.connect("classes.db") as conn:
        cur = conn.cursor()
        insertLesson = f""" INSERT INTO "Lessons"
        (unique_id,less_name,less_number,assignments,time)
        VALUES(
            2,"asdasd",2,"asdasf","asd"
        )"""
        cur.execute(insertLesson)
manager()