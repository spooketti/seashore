from prettytable import PrettyTable
import json
import argparse
import os
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).parent
SHEETS_DIR = BASE_DIR / "sheets"
MAIN_FILE = BASE_DIR / "main.txt"
SHEETS_DIR.mkdir(exist_ok=True) 

tableName = ""
table = PrettyTable()
todoTable = {}

def isJson(filename):
    return filename.endswith(".json")

parser = argparse.ArgumentParser()
parser.add_argument("-addCol","--addCol", type=str, help="Add a column to the current table: todo.sh addCol [NAME]")
parser.add_argument("-rmCol","--rmCol", type=str, help="Remove a column from the current table: todo.sh rmCol [NAME]")
parser.add_argument("-editCol","--editCol", type=str, help="Rename a column: todo.sh editCol [TORENAME] [NEWNAME]")
parser.add_argument("-write","--write", type=str, help="Write to a column: todo.sh write [COLUMNNAME] [CONTENT]")
parser.add_argument("-content","--content", type=str)
parser.add_argument("-index","--index", type=str)
parser.add_argument("-edit","--edit", type=str,help="Edit a value in a column: todo.sh edit [COLUMNNAME] [ROW#] [CONTENT]")
parser.add_argument("-erase","--erase", type=str,help="Erase a value in a column: todo.sh erase [COLUMNNAME] [ROW#]")
parser.add_argument("-clear","--clear", action=argparse.BooleanOptionalAction, help="Erase the entire board: todo.sh clear")

parser.add_argument("-lsTable","--lsTable", action=argparse.BooleanOptionalAction, help="Show all Tables: todo.sh lsTable")
parser.add_argument("-addTable","--addTable", type=str, help="Add a table: todo.sh addTable [NAME]")
parser.add_argument("-rmTable","--rmTable", type=str, help="Delete a table: todo.sh rmTable [NAME]")
parser.add_argument("-getTable","--getTable", type=str, help="View a noncurrent table: todo.sh getTable [NAME]")
parser.add_argument("-setTable","--setTable", type=str, help="Set a table to be current table to be edited by all previous commands: todo.sh setTable [NAME]")

args = parser.parse_args()


if(args.lsTable):
    print([Path(f).stem for f in os.listdir(SHEETS_DIR) if f.endswith(".json")])
    quit()

if(args.addTable):
    sheet = f"{args.addTable}.json"
    with open(SHEETS_DIR+sheet, 'w') as f:
        f.write("{}")
    print(f"Created {args.addTable} sheet")
    quit()


if(args.rmTable):
    os.remove(SHEETS_DIR+str(args.rmTable)+".json")
    quit()

if(args.setTable):
    tableName = args.setTable
    tableNameData = open(MAIN_FILE,"w")
    tableNameData.write(str(args.setTable))
    tableNameData.close()
    quit()

tableNameData = open(MAIN_FILE,"r")
tableName = str(tableNameData.read())
tableNameData.close()

if(args.getTable):
    tableName = args.getTable

with open(f"{SHEETS_DIR}/{tableName}.json","r") as todo:
   todoTable = json.load(todo)

if(args.addCol):
    todoTable[args.addCol] =  []
    
if(args.rmCol): 
    del todoTable[args.rmCol]

if(args.write):
    todoTable[args.write].append(args.content)

if(args.erase):
    del todoTable[args.erase][int(args.index)]

if(args.edit):
    todoTable[args.edit][int(args.index)] = args.content

if(args.editCol):
    todoTable[args.content] = todoTable.pop(args.editCol)

if(args.clear):
    todoTable = {}
    with open(f"{SHEETS_DIR}/{tableName}.json", "w") as json_file:
        json.dump(todoTable, json_file, indent=4)
    quit()

#the cookery
dynaTable = []
for title in todoTable:
    dynaTable.append(todoTable[title])
m = max(map(len, dynaTable))
dynaTable = np.array([v + [" "] * (m - len(v)) for v in dynaTable])
for i in range(len(list(todoTable))):
    table.add_column(list(todoTable.keys())[i],dynaTable[i])
    # table._max_width = {list(todoTable.keys())[i]: 10}
#end of the cookery

print('\033[93m' + "Current Table: "+tableName+'\033[0m')
print(table)


# print(table) todo.sh editCol ENM ABC

with open(f"{SHEETS_DIR}/{tableName}.json", "w") as json_file:
    json.dump(todoTable, json_file, indent=4)
