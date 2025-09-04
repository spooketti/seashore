from terminaltables import AsciiTable
import json
todoTable = {}
with open("todo.json","r") as todo:
    todoTable = json.load(todo)

table = AsciiTable(todoTable["main"])
print(table.table)
