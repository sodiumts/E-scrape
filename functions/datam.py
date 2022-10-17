import sqlite3 as sql
from os.path import exists
from datetime import date
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
                    date DATE,
                    PRIMARY KEY(unique_id)
                )
                """
                cur.execute(TestTable)

                DescTable = """ CREATE TABLE "Descriptions"(
                    unique_id INTEGER,
                    less_name TEXT,
                    less_number INTEGER,
                    less_desc TEXT,
                    time TEXT,
                    date DATE,
                    PRIMARY KEY(unique_id)
                )
                """
                cur.execute(DescTable)

                WholeTable = """ CREATE TABLE "Whole"()
                    unique_id INTEGER,
                    less_name TEXT,
                    less_number INTEGER,
                    less_desc TEXT,
                    time TEXT,
                    date DATE,
                    PRIMARY KEY(unique_id)
                """
    
    def insert_data_lessons(self,unique_id:int,lesson_name:str,number:int,task:str,times:str,date:date) -> None:
        with sql.connect("classes.db") as conn:
            curr = conn.cursor()
            curr.execute("SELECT rowid FROM Lessons WHERE unique_id = ?", (unique_id,))
            data = curr.fetchone()
            if data == None:
                tup = (unique_id,lesson_name,number,task,times,date)
                exec = f""" INSERT INTO "Lessons"
                (unique_id,less_name,less_number,assignments,time,date)
                VALUES(
                    ?,?,?,?,?,?
                )"""
                print("new data in Lessons at:",unique_id)
                curr.execute(exec,tup)
                return int(unique_id)
            
    def insert_data_test(self,unique_id:int,lesson_name:str,test_number:int,time:str,date:date) -> None:
        with sql.connect("classes.db") as conn:
            curr = conn.cursor()
            curr.execute("SELECT rowid FROM Tests WHERE unique_id = ?", (unique_id,))
            data = curr.fetchone()
            if data == None:
                tup = (unique_id,lesson_name,test_number,time,date)
                exec = f""" INSERT INTO "Tests"
                (unique_id,less_name,less_number,time,date)
                VALUES(
                    ?,?,?,?,?
                )"""
                print("new data in Tests at:",unique_id)
                curr.execute(exec,tup)
                return int(unique_id)


    def insert_data_descript(self,unique_id:int,lesson_name:str,less_number:int,lesson_desc:str,time:str,date:date) -> None:
        with sql.connect("classes.db") as conn:
            curr = conn.cursor()
            curr.execute("SELECT rowid FROM Descriptions WHERE unique_id = ?", (unique_id,))
            data = curr.fetchone()
            if data==None:
                tup = (unique_id,lesson_name,less_number,lesson_desc,time,date)
                exec = f""" INSERT INTO "Descriptions"
                (unique_id,less_name,less_number,less_desc,time,date)
                VALUES(
                    ?,?,?,?,?,?
                )"""
                print("new data in Descriptions at:",unique_id)
                curr.execute(exec,tup)
                return int(unique_id)
# db =DBManager()
# db.insert_data_lessons(-2134704900,"asd",1,"sas","sdas","20.09.2022")