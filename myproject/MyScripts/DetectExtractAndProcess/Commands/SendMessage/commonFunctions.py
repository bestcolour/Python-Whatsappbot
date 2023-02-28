
# keywords = {
#         "at","on" ,"every"
#     } 
def extract_keyword_info(splitMsg, keywords, keyWordToStartFrom):
    '''
    Extracts information between keywords from the list of messages inputed as arguement. Returns the information as a string. 
    >>> Eg. 
    keywords = {
        "at","on" ,"every"
    }   
    splitMsg = ["sd","at","12.34", "pm", "on","..."]

    usefulTimeInfo will be = ['12.34', 'pm']
    '''
    
    i = splitMsg.index(keyWordToStartFrom)
    usefulTimeInfo = []
    i += 1
    length = len(splitMsg)

    while splitMsg[i] not in keywords:
        usefulTimeInfo.append(splitMsg[i])
        i+= 1
        if(i >= length):
            break

    # print("Keyword: '{}' Extracted info: '{}'".format(keyWordToStartFrom,usefulTimeInfo))
    return usefulTimeInfo


def extract_keyword_info_with_spaces(msg,splitMsg, keywords, keyWordToStartFrom):
    '''
    Extracts information between keywords from the list of messages inputed as arguement without compromising on the whitespace in between the keywords. Returns the information as a string. 
    >>> Eg. 
    keywords = {
        "at","on" ,"every"
    }   
    splitMsg = ["sd","at","12.34", "pm", "on","..."]
    msg = "sd at 12.34 pm on ..."
    usefulTimeInfo will be = "12.34 pm"
    '''
    firstOccInSplit = splitMsg.index(keyWordToStartFrom)# find the first occurance of this keyword in splitmsg
    # now we find the first occurance of other keywords past the keyWordToStartFrom
    firstOccInSplit += 1
    length = len(splitMsg)

    #             Start -------> End
    # ["sd","at","12.34", "pm", "on","..."]
    # index will be 4
    while splitMsg[firstOccInSplit] not in keywords:
        firstOccInSplit+= 1
        if firstOccInSplit >= length:
            break

    # if index is less than length, this means that the index is the first occurance of a keyword after keyWordToStartFrom
    if firstOccInSplit < length:
        #  firstOccInSplit  is the index of the element in split Msg that is the keyword after keyWordToStartFrom
        firstOccInSplit = splitMsg[firstOccInSplit] # the key word after keyWordToStartFrom
        firstOccInSplit = msg.find(firstOccInSplit) #let firstOccInSplit hold the index of which the keywrod after keyWordToStartFrom is found in msg
        # substring
        firstOccInMsg = msg.find(keyWordToStartFrom) # find the first occurance of this keyword in msg
        firstOccInMsg += len(keyWordToStartFrom) # we want to start from after the keyword
        return msg[firstOccInMsg: firstOccInSplit]
    else:
    #else, that means that the keyword is the last keyword found until the end of the string
        # substring
        firstOccInMsg = msg.find(keyWordToStartFrom) # find the first occurance of this keyword in msg
        firstOccInMsg += len(keyWordToStartFrom) # we want to start from after the keyword
        return msg[firstOccInMsg:]

   

# print(extract_keyword_info_with_spaces(
#     keyWordToStartFrom= "to",
#     keywords= {"at","on" ,"every","to"},
#     msg= "sd at 12.34 pm on ...",
#     splitMsg= ["sd","at","12.34", "pm","on","..." ])
#     )
# # print(extract_keyword_info(["sd","at","12.34", "pm", "on","..."],keywords,"at"))