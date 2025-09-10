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
import plotext as plt
import numpy as np
from datetime import datetime
today = datetime.today()
today = str(today.strftime("%-d/%-m/%Y"))


plt.canvas_color("black") 
plt.axes_color("black")     
plt.ticks_color("white")     

linspace = np.linspace(0, 2*np.pi, 3)

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-gradebook","--gradebook", action=argparse.BooleanOptionalAction)
parser.add_argument("-graph","--graph", action=argparse.BooleanOptionalAction)
parser.add_argument("-startDate","--startDate", type=str)
parser.add_argument("-endDate","--endDate", type=str)
parser.add_argument("-classID","--classID", type=str)
args = parser.parse_args()

cache = {}
with open('cache.json', 'r') as file:
    cache = json.load(file)

sv = StudentVue(os.getenv("USERNAME"),os.getenv("PW"),os.getenv("URL"))
gb = sv.get_gradebook()
grades = sv.get_gradebook()
grades = grades["Gradebook"]["Courses"]["Course"]
payloadForCache = {"grades":{},"gradesGraph":{}}

hadChange = False
for key in grades:
    colorWarn = ''
    pValue = (key["Marks"]["Mark"]["@CalculatedScoreRaw"])
    if pValue < 90:
       colorWarn = terminalcolors.red
    payloadForCache["grades"][key["@Title"]] = pValue

    changeAmount = ""
    changeCode = ""
    changeCase = ""
    if pValue - cache["grades"][key["@Title"]] < 0:
        changeCode = terminalcolors.red
        changeAmount = f"-{str(abs(pValue-cache["grades"][key["@Title"]]))}%"
        changeCase = " " + changeCode + "(" + changeAmount + ")"+terminalcolors.end
        hadChange = True

    if pValue - cache["grades"][key["@Title"]] > 0:
        changeCode = terminalcolors.green
        changeAmount = f"+{str(pValue-cache["grades"][key["@Title"]])}%"
        changeCase = " " + changeCode + "(" + changeAmount + ")" + terminalcolors.end
        hadChange = True

    print(colorWarn + key["@Title"] + " " + str(key["Marks"]["Mark"]["@CalculatedScoreString"]) + " " + str(key["Marks"]["Mark"]["@CalculatedScoreRaw"]) + "%" +  terminalcolors.end + changeCase)
if(hadChange):
    payloadForCache["gradesGraph"] = cache["gradesGraph"]
    payloadForCache["gradesGraph"][today] =  payloadForCache["grades"]
    with open("cache.json", "w") as json_file:
        json.dump(payloadForCache, json_file,indent=4)
        cache = payloadForCache
    

def colorScore(s):
    try:
        num, denom = [float(x.strip()) for x in s.split('/')]
    except:
        return s
    value = num / denom
    color = next((c for t, c in [(0.9, terminalcolors.green), (0.85, terminalcolors.cyan), (0.8, terminalcolors.yellow)] if value >= t), terminalcolors.red)
    return f"{color} {s} {terminalcolors.end}"

def gradebook():
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

if(args.gradebook):
    gradebook()

if args.graph:
    #todo: startdate and enddate argument functionality
    records = sorted(
        r for r, grades in cache["gradesGraph"].items() if grades
    )
    subjects = set()
    for record in records:
        subjects.update(cache["gradesGraph"][record].keys())
    subjects = sorted(subjects)
    grade_data = {subject: [] for subject in subjects}
    for record in records:
        for subject in subjects:
            grade_data[subject].append(cache["gradesGraph"][record].get(subject, np.nan))
    for subject, grades in grade_data.items():
        plt.plot(records, grades, marker='x', label=subject)

    plt.xlabel("Time")
    plt.ylabel("Grade")
    plt.title("Grades Over Time")
    plt.show()
