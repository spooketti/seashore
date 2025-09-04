from prettytable import PrettyTable
import json
import argparse
import itertools
import numpy as np

table = PrettyTable()
todoTable = {}

parser = argparse.ArgumentParser()
parser.add_argument("-addCol","--addCol", type=str)
parser.add_argument("-rmCol","--rmCol", type=str)

parser.add_argument("-write","--write", type=str)
parser.add_argument("-content","--content", type=str)
parser.add_argument("-index","--index", type=str)
parser.add_argument("-edit","--edit", type=str)
parser.add_argument("-erase","--erase", type=str)

args = parser.parse_args()

with open("todo.json","r") as todo:
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

#the cookery
dynaTable = []
for title in todoTable:
    dynaTable.append(todoTable[title])
m = max(map(len, dynaTable))
dynaTable = np.array([v + [" "] * (m - len(v)) for v in dynaTable])
for i in range(len(list(todoTable))):
    table.add_column(list(todoTable.keys())[i],dynaTable[i])
#end of the cookery

print(table)


# print(table)

with open("todo.json", "w") as json_file:
    json.dump(todoTable, json_file, indent=4)
