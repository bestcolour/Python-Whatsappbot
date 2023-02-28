splitMsg = ["sd","at","12.34", "pm", "on"]

keywords = {
    "at","on" ,"every"
}


i = 0
for i in range(len(splitMsg)):
    if(splitMsg[i] == "at"):
        break

# at 12 pm on
usefulTimeInfo = []
i+= 1
length = len(splitMsg)

while splitMsg[i] not in keywords:
    usefulTimeInfo.append(splitMsg[i])
    i+= 1
    if(i >= length):
        break

print(usefulTimeInfo)