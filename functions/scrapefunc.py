import json
import requests
from datetime import date, datetime,timedelta
import bs4
import random
with open("details.json","r") as f:
    payloads = json.load(f)


days = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena","(šodien)","(rīt)","(parīt)","(vakar)","(aizvakar)"]

def dateTimeFormat(x,y):
    for day in days:
        x = x.replace(day, "").strip()
    
    times1,times2 = payloads["timetable"][y][0][0],payloads["timetable"][y][1][0]
    
    start,end = f"{x}.{times1}",f"{x}.{times2}"
    start,end = datetime.strptime(start, "%d.%m.%y..%H:%M"),datetime.strptime(end, "%d.%m.%y..%H:%M")
    return start,end

def scraper(payloads, weeks):
    #Open a requests session for retrieving data 
    with requests.Session() as s:
        #send post with credencials for login
        r = s.post("https://my.e-klase.lv/?v=15", data=payloads["payload1"], allow_redirects=True)
        #check if post was successful
        if r.url == "https://my.e-klase.lv/?v=15":
            print(f"Link missmatch post1: {r.url}")
            return 0x1 #invalid credentials
        elif r.status_code != 200:
            return 0x21,r.status_code #0x21 page offline for 1st post, or other issue

        #send post with tennant id and redirect url
        r = s.post("https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd",data=payloads["payload2"], allow_redirects=True)

        #check if post was successful part #2
        if r.url != "https://my.e-klase.lv/Family/Home":
            print(f"Link missmatch post2: {r.url}")
            return 0x3 #0x3 unknown error code, due to link missmatch
        elif r.status_code != 200:
            return 0x22,r.status_code #page offline for 2nd post, or other issue
        
        # for week in range(weeks):
        #     #get the dates for links
        #     dateForLink = date.today() + timedelta(days=7*week)
        #     #laod the current weeks page
        #     page = s.get(f"https://my.e-klase.lv/Family/Diary?Date={dateForLink}")

        #get the diary page contents of e-klase
        page = s.get("https://my.e-klase.lv/Family/Diary?Date=18.09.2022.")
        # print(r.status_code)
        #parse the html page
        page = bs4.BeautifulSoup(page.content,"html.parser")
        #find all elements with the class "hometask"
        homework_entries = page.find_all(class_="hometask")
        #go through all homework entries
        for entry in homework_entries:
            #find all <p> elements
            foundPelement = entry.findChildren("p")
            #go through all found <p> elements
            for element in foundPelement:
                #find the time and who added the assignment
                customIdSource = element.find_parent('span')["title"]
                #find the lesson number
                lessonNumberFound = element.find_parent("td").find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"number"})[0].text.strip()
                #find the task 
                foundTaskDate = element.find_parent("td").find_parent("table",{"class":"lessons-table"}).find_previous_sibling("h2").get_text().strip()
                #find the lesson name
                lessonName = element.find_parent("td").find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"title"})[0].text.strip()
                #generate a 32bit number as an identifier
                random.seed(a=customIdSource)
                print(random.randint(-2147483647,2147483647))

                print(" ".join(lessonName.split()))
                print(f"{dateTimeFormat(foundTaskDate,lessonNumberFound)[0]}-{dateTimeFormat(foundTaskDate,lessonNumberFound)[1]}")
                print(element.text)

def checkLoginData(username,password):
    payload1 = {
        "fake_pass":"",
        "UserName":username,
        "Password":password
    }
    with requests.Session() as s:
        r = s.post("https://my.e-klase.lv/?v=15", data=payload1, allow_redirects=True)

        if r.url == "https://my.e-klase.lv/?v=15":
            return 0x1 #invalid credentials
        elif r.status_code != 200:
            return 0x21
        #valid credentials
        return 0x200
scraper(payloads=payloads, weeks=1)