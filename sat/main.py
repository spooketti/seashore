import requests
import random
from markdownify import markdownify as md
from rich.console import Console
from rich.markdown import Markdown

class terminalcolors:
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'
    yellow = '\033[93m'

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
    "domain": "INI,CAS,EOI,SEC",
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

chosen_stub = random.choice(hard_stubs)
external_id = chosen_stub["external_id"]

payload = {"external_id": external_id}
r_q = session.post(QUESTION_URL, json=payload, timeout=5)
r_q.raise_for_status()
question_data = r_q.json()
question_data["difficulty"] = chosen_stub.get("difficulty")

print("External ID: " + external_id)

CONSOLE.print(Markdown(md(question_data.get("stimulus","").replace('<span class="sr-only">blank</span>',"").replace("<u>",terminalcolors.yellow).replace("</u>",terminalcolors.end))))
print("\n")
CONSOLE.print(Markdown(md(question_data.get("stem",""))))
print("\n")
answers = list(question_data.get("answerOptions",""))
ansChr = "A"

for i in answers:
    text =  "<span>" + ansChr + ")</span>" + str(i["content"])
    CONSOLE.print(Markdown(md(text)))
    ansChr = chr(ord(ansChr) + 1)
    print("\n")

answer = str(input())

if(answer.lower() != str(list(question_data.get("correct_answer",""))[0]).lower()):
    CONSOLE.print(Markdown(md(question_data.get("rationale",""))))
else:
    print(terminalcolors.green + "Locked In" + terminalcolors.end)