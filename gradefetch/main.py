class terminalcolors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'

from studentvue import StudentVue
from dotenv import load_dotenv
import json
import os
load_dotenv()

cache = {}
with open('cache.json', 'r') as file:
    cache = json.load(file)

sv = StudentVue(os.getenv("USERNAME"),os.getenv("PW"),os.getenv("URL"))
gb = sv.get_gradebook()
grades = sv.get_gradebook()
grades = grades["Gradebook"]["Courses"]["Course"]
payloadForCache = {}
for key in grades:
    colorWarn = ''
    pValue = (key["Marks"]["Mark"]["@CalculatedScoreRaw"])
    if pValue < 90:
       colorWarn = terminalcolors.red
    payloadForCache[key["@Title"]] = pValue

    changeAmount = ""
    changeCode = ""
    changeCase = ""
    if pValue - cache[key["@Title"]] < 0:
        changeCode = terminalcolors.red
        changeAmount = f"-{str(abs(pValue-cache[key["@Title"]]))}%"
        changeCase = " " + changeCode + "(" + changeAmount + ")"+terminalcolors.end
    if pValue - cache[key["@Title"]] > 0:
        changeCode = terminalcolors.green
        changeAmount = f"+{str(pValue-cache[key["@Title"]])}%"
        changeCase = " " + changeCode + "(" + changeAmount + ")" + terminalcolors.end

    print(colorWarn + key["@Title"] + " " + str(key["Marks"]["Mark"]["@CalculatedScoreString"]) + " " + str(key["Marks"]["Mark"]["@CalculatedScoreRaw"]) + "%" +  terminalcolors.end + changeCase)
with open("cache.json", "w") as json_file:
    json.dump(payloadForCache, json_file)
