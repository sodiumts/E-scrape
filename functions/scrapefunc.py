import json
import requests
from datetime import date, datetime,timedelta
import bs4
import random
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
    
    def insert_data_lessons(self,unique_id:int,lesson_name:str,number:int,task:str,times:str,date:date) -> int:
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
            
    def insert_data_test(self,unique_id:int,lesson_name:str,test_number:int,time:str,date:date) -> int:
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


    def insert_data_descript(self,unique_id:int,lesson_name:str,less_number:int,lesson_desc:str,time:str,date:date) -> int:
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

    def get_info(self,unique_id:int,relT:str) -> tuple:
        with sql.connect("classes.db") as conn:
            curr = conn.cursor()
            curr.execute(f"SELECT * FROM {relT} WHERE unique_id = ?", (unique_id,))
            data = curr.fetchone()
            print(data)
            print(type(data))
            return data    
class Scraper:
    def __init__(self):
        self.dataMan = DBManager()
        self.days = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena","(šodien)","(rīt)","(parīt)","(vakar)","(aizvakar)"]
        self.times = {"0.": ["07:35","08:15"],
                "1.": ["08:20","09:00"],
                "2.": ["09:10","09:50"],
                "3.": ["10:00","10:40"],
                "4.": ["10:50","11:30"],
                "5.": ["11:40","12:20"],
                "6.": ["12:30","13:10"],
                "7.": ["13:20","14:00"],
                "8.": ["14:10","14:50"],
                "9.": ["15:00","15:40"],
                "10.": ["15:50","16:30"]}
        with open("functions/details.json","r") as f:
            self.creds = json.load(f)
    def get_main_page(self,weeks) -> list:
         #Open a requests session for retrieving data 
        with requests.Session() as s:
            #send post with credencials for login
            r = s.post("https://my.e-klase.lv/?v=15", data=self.creds["creds"], allow_redirects=True)
            #check if post was successful
            if r.url == "https://my.e-klase.lv/?v=15":
                print(f"Link missmatch post1: {r.url}")
                return 0x1 #invalid credentials
            elif r.status_code != 200:
                return 0x21,r.status_code #0x21 page offline for 1st post, or other issue

            #send post with tennant id and redirect url
            r = s.post("https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd",data=self.creds["tenID"], allow_redirects=True)

            #check if post was successful part #2
            if r.url != "https://my.e-klase.lv/Family/Home":
                print(f"Link missmatch post2: {r.url}")
                return 0x3 #0x3 unknown error code, due to link missmatch
            elif r.status_code != 200:
                return 0x22,r.status_code #page offline for 2nd post, or other issue
            pages = []
            for week in range(weeks):
                #get the dates for links
                dateForLink = date.today() + timedelta(days=7*week)
                #laod the current weeks page
                page = s.get(f"https://my.e-klase.lv/Family/Diary?Date={dateForLink}")
                page = bs4.BeautifulSoup(page.content,"html.parser")
                pages.append(page)

            #get the diary page contents of e-klase
            # page = s.get("https://my.e-klase.lv/Family/Diary?Date=18.09.2022.")
            # print(r.status_code)
            #parse the html page
            return pages

    def scrape_homework(self,**kwargs) -> list:
        if kwargs.get("preloaded",None):
            pages = kwargs.get("preloaded",None)
        else:
            weeks = kwargs.get("weeks",None)
            pages = self.get_main_page(weeks)
        NewEntries = []
        for page in pages:
        #find all elements with the class "hometask"
            homework_entries = page.find_all(class_="hometask")
            #go through all homework entries
            for entry in homework_entries:
                #find all <p> elements
                foundelements = entry.findChildren()
                if foundelements:
                    # print(foundelements)
                    try:
                        customIdSource = foundelements[0]["title"]
                    except:
                        # print("EXCEPTION")
                        if foundelements[0].findChildren("div",{"class":"home-task-answer-widget"}):
                            customIdSource = foundelements[0].text.strip()

                    

                    lessonNumberFound= entry.find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"number"})[0].text.strip()
                    lessonName = entry.find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"title"})[0].text.strip()
                    tasks =[]
                    for elements in entry:
                        tasks.append(elements.text.strip())
                    mainTask = "\n".join([str(elem) for elem in tasks]).strip()
                    taskDate = str(entry.find_parent("table",{"class":"lessons-table"}).find_previous_sibling("h2").text.strip())
                    for day in self.days:
                        try:
                            taskDate = taskDate.replace(day,"")
                        except:
                            continue
                    customIdSource = customIdSource + str(lessonNumberFound)
                    unique_seed=random.seed(a=customIdSource)
                    unique_id=random.randint(-2147483647,2147483647)

                    timeFormatted = self.times[lessonNumberFound]

                    timeFormatted = self.times[lessonNumberFound]
                    timeFormatted = str(f"{timeFormatted[0]} - {timeFormatted[1]}")
                    taskDateConv = datetime.strptime(taskDate.strip(),"%d.%m.%y.")
                    # print(taskDateConv)
                    news = self.dataMan.insert_data_lessons(unique_id,lessonName,lessonNumberFound,mainTask,timeFormatted,taskDateConv)
                    if news != None:
                        NewEntries.append(news)
        if NewEntries:
            return NewEntries
        else:
            return None
    def scrape_tests(self,**kwargs) -> list:
        if kwargs.get("preloaded",None):
            pages = kwargs.get("preloaded",None)
        else:
            weeks = kwargs.get("weeks",None)
            pages = self.get_main_page(weeks)
        NewEntries = []
        for page in pages:
            foundTest = page.find_all("span",{"class":"subject--scheduledTest"})
            # print(foundTest)
            for test in foundTest:
                foundTestParent = test.find_parent("td")
                if foundTestParent == None:
                    break
                foundTestSubject = foundTestParent.find_previous_sibling("td").findChildren("span",{"class":"title"})[0].text.strip()
                foundTestNumber = foundTestParent.find_previous_sibling("td").findChildren("span",{"class":"number"})[0].text.strip()
                foundTestDate = foundTestParent.find_parent("table",{"class":"lessons-table"}).find_previous_sibling().text.strip()
                for day in self.days:
                        try:
                            foundTestDate = foundTestDate.replace(day,"")
                        except:
                            continue
                testDateConv = datetime.strptime(foundTestDate.strip(),"%d.%m.%y.")
                unique_seed = random.seed(a=foundTestSubject+foundTestDate)
                unique_id = random.randint(-2147483647,2147483647)
                timeFormatted = self.times[foundTestNumber]
                timeFormatted = str(f"{timeFormatted[0]} - {timeFormatted[1]}")
                
                news =self.dataMan.insert_data_test(unique_id,foundTestSubject,foundTestNumber,timeFormatted,testDateConv)
                if news != None:
                    NewEntries.append(news)
        if NewEntries:
            return NewEntries
        else:
            return None

    def scrape_descriptions(self,**kwargs) -> list:
        if kwargs.get("preloaded",None):
            pages = kwargs.get("preloaded",None)
        else:
            weeks = kwargs.get("weeks",None)
            pages = self.get_main_page(weeks)
        NewEntries = []
        for page in pages:
            instanceIfNoNumber = 0
            foundDesc = page.find_all("td",{"class":"subject"})
            for desc in foundDesc:
                if desc.find_parent("tr").find_previous_sibling("tr") == None:
                    continue
                if desc.find_previous_sibling("td").findChildren("span",{"class":"number--lessonNotInDay"}):
                    foundDescNumber = "After classes"
                    instanceIfNoNumber+=1
                    foundDescDate = desc.findParent("table",{"class":"lessons-table"}).find_previous_sibling("h2").text.strip()
                    for day in self.days:
                        try:
                            foundDescDate = foundDescDate.replace(day,"")
                        except:
                            continue
                    customidSource = str(foundDescNumber) + str(instanceIfNoNumber) + str(foundDescDate)
                    unique_seed = random.seed(a=customidSource)
                    unique_id = random.randint(-2147483647,2147483647)
                    timeFormatted = "After classes"
                    descDateConv = datetime.strptime(foundDescDate.strip(),"%d.%m.%y.")

                else:
                    foundDescNumber = desc.find_previous_sibling("td").findChildren("span",{"class":"number"})[0].text.strip()
                    foundDescDate = desc.findParent("table",{"class":"lessons-table"}).find_previous_sibling("h2").text.strip()
                    customidSource = str(foundDescNumber) + str(foundDescDate)
                    for day in self.days:
                        try:
                            foundDescDate = foundDescDate.replace(day,"")
                        except:
                            continue
                    unique_seed = random.seed(a=customidSource)
                    unique_id = random.randint(-2147483647,2147483647)
                    timeFormatted = self.times[foundDescNumber]
                    timeFormatted = str(f"{timeFormatted[0]} - {timeFormatted[1]}")
                    descDateConv = datetime.strptime(foundDescDate.strip(),"%d.%m.%y.")
                    
                
                foundDescTitle = desc.find_previous_sibling("td").findChildren("span",{"class":"title"})[0].text.strip()
                foundDescContent = desc.text.strip()
                # print(unique_id,foundDescTitle,foundDescNumber,foundDescContent,timeFormatted,descDateConv)
                news = self.dataMan.insert_data_descript(unique_id,foundDescTitle,foundDescNumber,foundDescContent,timeFormatted,descDateConv)
                if news != None:
                    NewEntries.append(news)
        if NewEntries:
            return NewEntries
        else:
            return None
    
    def scrape_all(self,weeks)->dict:
        output = {
            "NewHomework":[],
            "NewTests":[],
            "NewDescriptions":[],
        }
        pages = self.get_main_page(weeks)

        newHW = self.scrape_homework(preloaded=pages)
        newTS = self.scrape_tests(preloaded=pages)
        newDS = self.scrape_descriptions(preloaded=pages)

        output["NewDescriptions"] = newDS
        output["NewHomework"] = newHW
        output["NewTests"] = newTS
        return output
    def checkLoginData(self,username,password):
        creds = {
            "fake_pass":"",
            "UserName":username,
            "Password":password
        }
        with requests.Session() as s:
            r = s.post("https://my.e-klase.lv/?v=15", data=creds, allow_redirects=True)

            if r.url == "https://my.e-klase.lv/?v=15":
                return 0x1 #invalid credentials
            elif r.status_code != 200:
                return 0x21
            #valid credentials
            return 0x200

    
s = DBManager()
s.get_info(1506239581,"Lessons")
