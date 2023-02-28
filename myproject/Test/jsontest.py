import json


x = {
    "groupchatname": "chat1234",
    "duedate": {
        "time": 123,
        "date": 432
    }
}


jsonFormat= json.dumps(x,indent=4)
print(jsonFormat)

dictionary = json.loads(jsonFormat)
print(dictionary["duedate"]["time"])
