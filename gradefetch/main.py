class terminalcolors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    cyan = '\033[96m'

from studentvue import StudentVue
from dotenv import load_dotenv
import argparse
import json
import os
from fractions import Fraction
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-gradebook","--gradebook", action=argparse.BooleanOptionalAction)
parser.add_argument("-classID","--classID", type=str)
args = parser.parse_args()

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

if(not args.gradebook):
    quit()

def colorScore(s):
    try:
        num, denom = [float(x.strip()) for x in s.split('/')]
    except:
        return s
    value = num / denom
    color = next((c for t, c in [(0.9, terminalcolors.green), (0.85, terminalcolors.cyan), (0.8, terminalcolors.yellow)] if value >= t), terminalcolors.red)
    return f"{color} {s} {terminalcolors.end}"

print(terminalcolors.yellow + "================================GRADEBOOK================================" + terminalcolors.end)
courses = gb["Gradebook"]["Courses"]["Course"]
for grade in courses:
    if(not str(args.classID) in grade["@Title"]):
        continue
    assignments = grade["Marks"]["Mark"]['Assignments']
    try:
        for assignment in assignments["Assignment"]:
            noScore = False
            try:
                last_measure = assignment["@Measure"]
                score = assignment["@Score"]
                if "Not" in str(score):
                    print(assignment["@Measure"] + terminalcolors.red + "Score Pending" + terminalcolors.end)
                    noScore = True
            except:
                if "Not" in str(assignment):
                    print(assignment["@Measure"] + terminalcolors.red + "Score Pending" + terminalcolors.end)
                    noScore = True
            if(noScore):
                continue
            print(str(assignment["@Measure"]) + (colorScore(assignment["@Points"])))
    except:
        pass