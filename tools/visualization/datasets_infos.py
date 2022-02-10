import json


result = None

with open("data/table/annotations/latex_train.json") as f:
    print(type(f))  # <class '_io.TextIOWrapper'>  也就是文本IO类型
    result=json.load(f)

print(result)