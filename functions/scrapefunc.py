import json
import requests
from datetime import date, datetime,timedelta
import bs4
import random
import datam
with open("details.json","r") as f:
    creds = json.load(f)

dataMan = datam.DBManager()
days = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena","(šodien)","(rīt)","(parīt)","(vakar)","(aizvakar)"]
times = {"0.": ["07:35","08:15"],
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


def scraper(creds, weeks):
    #Open a requests session for retrieving data 
    with requests.Session() as s:
        #send post with credencials for login
        r = s.post("https://my.e-klase.lv/?v=15", data=creds["creds"], allow_redirects=True)
        #check if post was successful
        if r.url == "https://my.e-klase.lv/?v=15":
            print(f"Link missmatch post1: {r.url}")
            return 0x1 #invalid credentials
        elif r.status_code != 200:
            return 0x21,r.status_code #0x21 page offline for 1st post, or other issue

        #send post with tennant id and redirect url
        r = s.post("https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd",data=creds["tenID"], allow_redirects=True)

        #check if post was successful part #2
        if r.url != "https://my.e-klase.lv/Family/Home":
            print(f"Link missmatch post2: {r.url}")
            return 0x3 #0x3 unknown error code, due to link missmatch
        elif r.status_code != 200:
            return 0x22,r.status_code #page offline for 2nd post, or other issue
        
        for week in range(weeks):
            #get the dates for links
            dateForLink = date.today() + timedelta(days=7*week)
            #laod the current weeks page
            page = s.get(f"https://my.e-klase.lv/Family/Diary?Date={dateForLink}")

        #get the diary page contents of e-klase
        # page = s.get("https://my.e-klase.lv/Family/Diary?Date=18.09.2022.")
        # print(r.status_code)
        #parse the html page
        page = bs4.BeautifulSoup(page.content,"html.parser")
        #find all elements with the class "hometask"
        homework_entries = page.find_all(class_="hometask")
        #go through all homework entries
        for entry in homework_entries:
            #find all <p> elements
            foundelements = entry.findChildren()
            if foundelements:
                customIdSource = foundelements[0]["title"]
                lessonNumberFound= entry.find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"number"})[0].text.strip()
                lessonName = entry.find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"title"})[0].text.strip()
                tasks =[]
                for elements in entry:
                    tasks.append(elements.text.strip())
                mainTask = "\n".join([str(elem) for elem in tasks]).strip()
                taskDate = str(entry.find_parent("table",{"class":"lessons-table"}).find_previous_sibling("h2").text.strip())
                for day in days:
                    try:
                        taskDate = taskDate.replace(day,"")
                    except:
                        continue
                unique_seed=random.seed(a=customIdSource)
                unique_id=random.randint(-2147483647,2147483647)

                timeFormatted = times[lessonNumberFound]

                timeFormatted = times[lessonNumberFound]
                timeFormatted = str(f"{timeFormatted[0]} - {timeFormatted[1]}")
                taskDateConv = datetime.strptime(taskDate.strip(),"%d.%m.%y")
                print(taskDateConv)
                dataMan.insert_data(unique_id,lessonName,lessonNumberFound,mainTask,timeFormatted,taskDate.strip())
                


def checkLoginData(username,password):
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
scraper(creds=creds, weeks=2)