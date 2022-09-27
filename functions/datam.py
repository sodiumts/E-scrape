import sqlite3 as sql
from os.path import exists
import datetime
class DBManager:
    def __init__(self) -> None:
        if exists("classes.db") == False:
                    with sql.connect("classes.db") as conn:
                        cur = conn.cursor()
                        LessonTable = """ CREATE TABLE "Lessons"(
                            unique_id INTEGER,
                            less_name TEXT,
                            less_number INTEGER,
                            assignments TEXT,
                            time TEXT,
                            date DATE,
                            PRIMARY KEY(unique_id)
                        )
                        """
                        cur.execute(LessonTable)
                        TestTable = """ CREATE TABLE "Tests"(
                            unique_id INTEGER,
                            less_name TEXT,
                            less_number INTEGER,
                            time TEXT,
                            date TEXT,
                            PRIMARY KEY(unique_id)
                        )
                        """
                        cur.execute(TestTable)

    def insert_data(self,unique_id:int,lesson_name:str,number:int,task:str,times:str,date:datetime.date) -> None:
        with sql.connect("classes.db") as conn:
            curr = conn.cursor()
            tup = (unique_id,lesson_name,number,task,times,date)
            exec = f""" INSERT INTO "Lessons"
            (unique_id,less_name,less_number,assignments,time,date)
            VALUES(
                ?,?,?,?,?,?
            )"""
            curr.execute(exec,tup)