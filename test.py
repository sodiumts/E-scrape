from datetime import date, datetime, time
days = ["pirmdiena","otrdiena","trešdiena","ceturtdiena","piektdiena"]
import json
import telegram_send
f = open("details.json")
payloads = json.load(f)

time_table = payloads["timetable"]
#print(time_table)
foundTestTime="2."
#print(list(time_table["timetable"].keys())[list(time_table["timetable"].values()).index(foundTestTime)])
DATEVARIABLE = "14.12.21. trešdiena"

#print(time_table[foundTestTime])
# for day in days:
#     print(DATEVARIABLE.replace(day,"").strip())
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
array = dateTimeFormat(DATEVARIABLE,foundTestTime)
print(array[0])
#print(dateTimeFormat(DATEVARIABLE,foundTestTime))
