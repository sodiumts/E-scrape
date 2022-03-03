from typing import TypedDict
import bs4
import requests
from requests.api import request
from requests.sessions import session
from datetime import date, timedelta, datetime
import json
import telegram_send
f = open("details.json")
payloads = json.load(f)
# tagSpan = bs4.span

payload1 = payloads["payload1"]
payload2 = payloads["payload2"]
days = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena","(šodien)","(rīt)","(parīt)","(vakar)"]
time_table = payloads["timetable"]
today = date.today()
weeks = 2
# date_1 = today + timedelta(days=7*x)
# finalDate = date_1.strftime("%d.%m.%y")
# print(finalDate)

def pret(y):
    y=bs4.BeautifulSoup(y.content,"html.parser")
    return y

def printType(x):
    print(x, type(x)) 

def lookupTime(x):
    x=list(time_table.keys())[list(time_table.values()).index(x)]
    return x
    
def dateTimeFormat(x,y):
    for day in days:
        x = x.replace(day, "").strip()

    times1 = time_table[y][0][0]
    times2 = time_table[y][1][0]
    z = f"{x}.{times1}"
    w = f"{x}.{times2}"
    z = datetime.strptime(z, "%d.%m.%y..%H:%M")
    w = datetime.strptime(w, "%d.%m.%y..%H:%M")
    return [z,w]





#print(time_table)
with requests.Session() as s:
    r = s.post("https://my.e-klase.lv/?v=15", data=payload1, allow_redirects=True)
    #print(r.url)
    #print(pret(r))
    r = s.post("https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd", data=payload2)
    #print(r.url)
    for week in range(weeks):
        print(week)
        date_1 = today + timedelta(days=7*week)
        finalDate = date_1.strftime("%d.%m.%Y.")
        page = s.get(f"https://my.e-klase.lv/Family/Diary?Date={finalDate}")#{finalDate}
        # print(page.url)
        print(f"https://my.e-klase.lv/Family/Diary?Date={finalDate}")
        #print(page.url)
        """Finding the tests by using the class 'subject--scheduledTest'
        to locate the td elements that contain a test. 
        Iterate through all of the foundTest bs4.resultsList putting 
        each element in variable i and finding the subject name with test"""
        if page.status_code == 200:
            page_contents = pret(page)
            ########################################################################
            foundTest = page_contents.find_all(class_="subject--scheduledTest")
            #print(page_contents)
            for i in foundTest:
                try:
                    foundTest = i.find_parent("td").find_previous_sibling("td").findChildren("span",{"class":"title"})[0].get_text().strip()
                    foundTestDate = i.find_parent("table",{"class":"lessons-table"}).find_previous_sibling("h2").get_text().strip()
                    foundTestTime = i.find_parent("td").find_previous_sibling("td").findChildren("span",{"class":"number"})[0].get_text().strip()
                    #print(lookupTime(foundTestTime))
                    testDateTimeArray=dateTimeFormat(foundTestDate,foundTestTime)
                    sendStr = foundTest+"\n"+str(testDateTimeArray[0].strftime("%d.%m.%Y.")+"\n"+testDateTimeArray[0].strftime("%H:%M")+"-"+ str(testDateTimeArray[1].strftime("%H:%M")))
                    #print(sendStr)
                    date_1.strftime("%d.%m.%Y.")
                    #telegram_send.send(messages=[sendStr])
                    #test_date=datetime.strptime(foundTestDate)
                    #printType(datetime_test_object)
                except Exception as e:
                    #print(e)
                    break
            Homework = page_contents.find_all(class_="hometask")
            #printType(Homework)
            for home in Homework:
                #print(home)
                    foundHome = home.findChildren("p")
                    #printType(foundHome)
                    try:
                        #foundHome[0].text
                        for element in foundHome:
                            lessonNumberFound = element.find_parent("td").find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"number"})[0].text.strip()
                            foundTestDate = element.find_parent("td").find_parent("table",{"class":"lessons-table"}).find_previous_sibling("h2").get_text().strip()
                            lessonName = element.find_parent("td").find_previous_sibling("td",{"class":"first-column"}).findChildren("span",{"class":"title"})[0].text.strip()

                            # try:
                            #     lessonName.trim()
                            # except:
                            #     continue

                            printType(lessonName)
                            taskDateTimeArray = dateTimeFormat(foundTestDate,lessonNumberFound)
                            #printType(element)
                            printType(taskDateTimeArray)
                            sendStr = str(lessonName)+"\n"+f"<b><i>MD: {element.text}</i></b>"+"\n"+str(taskDateTimeArray[0].strftime("%d.%m.%Y.")+"\n"+taskDateTimeArray[0].strftime("%H:%M")+"-"+ str(taskDateTimeArray[1].strftime("%H:%M")))
                            #print(sendStr)
                            telegram_send.send(messages=[sendStr], parse_mode='HTML')#messages=[sendStr]
                        #printType(foundHome)
                    except Exception as e:
                        print(e)
                        continue

        else:
            print("error:",page.url, page.status_code)
