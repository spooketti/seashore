from prettytable import PrettyTable
import json
import argparse

table = PrettyTable()
todoTable = {}

parser = argparse.ArgumentParser()
parser.add_argument("-addCol","--addCol", type=str)
parser.add_argument("-rmCol","--rmCol", type=str)
args = parser.parse_args()

with open("todo.json","r") as todo:
   todoTable = json.load(todo)

if(args.addCol):
    todoTable[args.addCol] =  [""] * len(todoTable[list(todoTable.keys())[0]])
    
if(args.rmCol): 
    del todoTable[args.rmCol]

for title in todoTable:
    table.add_column(title,todoTable[title])

print(table)

with open("todo.json", "w") as json_file:
    json.dump(todoTable, json_file, indent=4)
