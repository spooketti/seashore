import requests
import argparse
import random
from markdownify import markdownify as md
from rich.console import Console
from rich.markdown import Markdown
import plotext as plt
import time

class terminalcolors:
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'
    yellow = '\033[93m'

parser = argparse.ArgumentParser()
parser.add_argument("-quiz","--quiz",action=argparse.BooleanOptionalAction)
args = parser.parse_args()

plt.canvas_color("black")
plt.axes_color("black")
plt.ticks_color("white")

CONSOLE = Console()
METADATA_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions"
QUESTION_URL = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question"

HEADERS = {
    "Accept":       "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin":       "https://satsuitequestionbank.collegeboard.org",
    "Referer":      "https://satsuitequestionbank.collegeboard.org/",
}

payload = {
    "asmtEventId": 99,
    "test": 1, #lowk if anyone sees this could you tell me about what this means
    "domain": "INI,SEC,CAS,EOI",
}

session = requests.Session()
session.headers.update(HEADERS)

request = session.post(METADATA_URL, json=payload, timeout=5)
request.raise_for_status()
metadata_list = request.json()

hard_stubs = [
    stub for stub in metadata_list
    if str(stub.get("difficulty", "")).lower() in ["hard", "h"]
]

if not hard_stubs:
    raise ValueError("No hard questions found in metadata list!")

run = True
runCount = 0
correct = 0
questionData = []

def answerCheck(answer):
    global run
    global correct
    global questionData

    user = answer.lower()
    correct_answer = str(questionData.get("correct_answer", "")[0]).lower()
    match user:
        case "q" | "quit":
            run = False
        case _ if user == correct_answer:
            print(terminalcolors.green + "Locked In" + terminalcolors.end)
            correct += 1
        case _:
            CONSOLE.print(Markdown(md(questionData.get("rationale", ""))))

percentageData = []
while(run):
    run = not(args.quiz is None)
    color = terminalcolors.green
    percent = (correct/max(1,runCount))
    if(percent < (49/54)):
        color = terminalcolors.red
    percent *= 100
    percentageData.append(percent)
    percent = " " + str(percent) + "%"
    startTime = time.time()

    print("Question " + str(runCount+1))

    print(color + "Score: " + str(correct) + "/" + str(runCount) + percent + terminalcolors.end)
    runCount += 1
    chosen_stub = random.choice(hard_stubs)
    external_id = chosen_stub["external_id"]

    payload = {"external_id": external_id}
    r_q = session.post(QUESTION_URL, json=payload, timeout=5)
    r_q.raise_for_status()
    questionData = r_q.json()
    questionData["difficulty"] = chosen_stub.get("difficulty")

    print("External ID: " + external_id)

    CONSOLE.print(Markdown(md(questionData.get("stimulus","").replace('<span class="sr-only">blank</span>',"").replace("<u>",terminalcolors.yellow).replace("</u>",terminalcolors.end))))
    print("\n")
    CONSOLE.print(Markdown(md(questionData.get("stem",""))))
    print("\n")
    answers = list(questionData.get("answerOptions",""))
    ansChr = "A"

    for i in answers:
        text =  "<span>" + ansChr + ")</span>" + str(i["content"])
        CONSOLE.print(Markdown(md(text)))
        ansChr = chr(ord(ansChr) + 1)
        print("\n")

    answer = str(input())
    print(terminalcolors.yellow + "Time (s): " + str(time.time()-startTime) + terminalcolors.end)
    answerCheck(answer)

if not(args.quiz):
    quit()

percentageData.pop(0)
x = list(range(len(percentageData)))
y = percentageData

plt.plot(x, y)
plt.title("Performance Over Time")
plt.xlabel("Question")
plt.ylabel("Percentage")
plt.show()

