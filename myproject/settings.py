'''
\nIs the file that contains all the XPath of various whatsapp web ui elements and other controls for the bot to follow.
'''

import json
import pytz
from pydoc import locate

#region === Save Load Functions ===
def save_dictionary(filePath,jsonString):
    with open (filePath,"w") as outfile:
        outfile.write(jsonString)

def load_dictionary(filePath):
    '''
    \nReads from the data json file returns the json data (loaded) as string
    '''
    try:
        with open (filePath) as jsonFile:
            return json.load(jsonFile)
    except:
        return None



#endregion
    

PATH_DATA_JSON = "data.json"
'''
The path of the data json
'''

PATH_XPATH_SETTINGS_JSON = "xpath_settings.json"
PATH_BOT_SETTINGS_JSON = "bot_settings.json"


#region xpath settings
xpath_settings_dict = {

#region driverManager.py
"XPATH_QR_CODE_ELEMENT":  "//canvas[@aria-label='Scan me!']",
"XPATH_QR_CODE_ELEMENT_C":"The xpath of the QR code element whenever whatsapp web is loaded",

"LINK_WHATSAPP_WEBPAGE":  "https://web.whatsapp.com/",
"LINK_WHATSAPP_WEBPAGE_C":"The link of whatsapp webapge ",


#endregion

# region msgExtractionFunc.py
# in order to replace this, search for "XPATH_MESSAGE_TEXT" in the files and replace the XPath directly and not here. This is because for some reason, the exact same path doesnt work when the variable is passed into the function
# important to have '.' infront
"XPATH_MESSAGE_TEXT":  ".//span[@class='_11JPr selectable-text copyable-text']",
"XPATH_MESSAGE_TEXT_C":"The xpath of the message element in any conversation chat",

"XPATH_PARENT_OF_ROWS":  "//div[@role='application']",
"XPATH_PARENT_OF_ROWS_C":"The xpath of the parent element that holds all of the row elements (which holds the messages and their time,etc)",

"XPATH_MATCHED_TEXT":  "//span[(@title='{}')]" ,
"XPATH_MATCHED_TEXT_C":"format this with the group name to get the matched text of the groupname",

"XPATH_GROUP_SEARCH_BOX":  "//div[(@data-testid='chat-list-search')]",
"XPATH_GROUP_SEARCH_BOX_C":"The xpath of the search box/bar when you are searching for a groupchat to enter into focus",

# endregion

# region detectMsgFunctions.py
"XPATH_UNREAD_MSG_ICON":  "//span[@data-testid='icon-unread-count']",
"XPATH_UNREAD_MSG_ICON_C":"The xpath of the unread message icon (the green circle with the numbers inside of it)",

# XPATH_MESSAGE_REPLYBUTTON = "//li[@data-testid='mi-msg-reply']"
"XPATH_MESSAGE_TIME":  "//div[@data-testid='msg-meta']",
"XPATH_MESSAGE_TIME_C":"The xpath of the message's time element",

"XPATH_MESSAGE_INPUT_FIELD":  "//div[@data-testid='conversation-compose-box-input']",
"XPATH_MESSAGE_INPUT_FIELD_C":"The xpath of the conversation input field when there is a focused chatgroup.",

"XPATH_GROUPCHAT_TITLE":  "//span[@data-testid='conversation-info-header-chat-title']",
"XPATH_GROUPCHAT_TITLE_C":"The xpath to get the current focused chat group's groupname",

# endregion

#region sendMessageCommands
"LINK_START_CONVO_WITH_NEW_NUM":  "https://wa.me/" ,
"LINK_START_CONVO_WITH_NEW_NUM_C":"This link is the start of the send message to new phone number conversation process. This string must be followed with a phonenumber (including the country code minus the +)",

"XPATH_CONTINUE_TO_CHAT_BUTTON":  "//a[@id='action-button']",
"XPATH_CONTINUE_TO_CHAT_BUTTON_C":"The first button that needs to be pressed after opening the link 'https://wa.me/+phoneNum' when sending messages to a new contact number.",

"XPATH_USE_WHATSAPP_WEB_HYPERLINK":  ".//a[@href='https://web.whatsapp.com/send/?phone={}&text&type=phone_number&app_absent=0']",
"XPATH_USE_WHATSAPP_WEB_HYPERLINK_C":"Format the intended phone number you want to message in between to get the hyperlink that we need to click on",

"ID_FALLBACK_BLOCK":  "fallback_block",
"ID_FALLBACK_BLOCK_C":"This is the id of the html which is the parent of the hyperlink we are looking for",


#endregion

}
#endregion


#region Bot Settings
bot_settings_dict = {
"TIMEZONE" : "Singapore",
"TIMEZONE_C":"The timezone in which the bot will use as reference to sending all the messages with. Visit https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 to see all available timezones.\nDefault value is 'Singapore'",
"TIMEZONE_T":"str",

"GROUPCHAT_SEARCH_PAUSE" : 1,
"GROUPCHAT_SEARCH_PAUSE_C":"\nThe duration in which the bot pauses after searching for the group chat name and before clicking on the matched group chat. Longer value means more time for the matched group chat element to load (which could be better on slower internet connections)\n\nDefault value is 1",
"GROUPCHAT_SEARCH_PAUSE_T":"float",

"CONVO_INPUT_PAUSE" : 0.3,
"CONVO_INPUT_PAUSE_C":"\nThe duration in which the bot pauses after copying and pasting text into the conversation input box field. Lower values may result in the text being cut off but faster type speed.\n\nDefault value is 0.3",
"CONVO_INPUT_PAUSE_T":"float",

"MSG_NEW_NUMBER_PAUSE" : 5,
"MSG_NEW_NUMBER_PAUSE_C":"\nThe duration for whenever the bot messages a new number and needs to wait for the whatsappweb page to load fully again, starting the conversation with the new number.\n\nDefault value is 5",
"MSG_NEW_NUMBER_PAUSE_T":"float",

"AUTO_SAVE_FREQUENCY" : 60,
"AUTO_SAVE_FREQUENCY_C":"The number of seconds that needs to pass before the bot auto saves the ongoing commands\n\nDefault value is 60",
"AUTO_SAVE_FREQUENCY_T":"float",

"SAVE_WHENVER_A_COMMAND_HAS_BEEN_COMPLETED" : 1,
"SAVE_WHENVER_A_COMMAND_HAS_BEEN_COMPLETED_C":"Saves whenever a command has finished it's task. Input 1 to set it to True else, input 0\n\nDefault value is 1(True)",
"SAVE_WHENVER_A_COMMAND_HAS_BEEN_COMPLETED_T":"int",

"ADMIN_NUMBERS" : [],
"ADMIN_NUMBERS_C":"Set the admin numbers list (eg. +6591234567, +6597654321) to allow additional features such as:\n-sending messages to other groups\n-sending messages to phone numbers/contacts.\n\nHowever, you must be sending those commands specifically in a chat to the bot's number in order to use these features.",
"ADMIN_NUMBERS_T":"list",

"MAX_NUM_OF_TRIES_B4_CMD_REMOVES_ITSELF" : 3,
"MAX_NUM_OF_TRIES_B4_CMD_REMOVES_ITSELF_C":"The number of attempts the bot will try to execute a command before it automatically removes itself from the system\n\nDefault value is 3",
"MAX_NUM_OF_TRIES_B4_CMD_REMOVES_ITSELF_T":"int"
}

#endregion


#region Get Set Functions
def get(key):
    global xpath_settings_dict
    global bot_settings_dict
    
    x = xpath_settings_dict.get(key)
    if x != None:
        return x

    x = bot_settings_dict.get(key)
    if x != None:
        return x
    
    print("The key: '{}' is not found in settings".format(key))


def set(key,value):
    global bot_settings_dict,PATH_BOT_SETTINGS_JSON
    typeCast = bot_settings_dict[key+"_T"]
    typeCast = locate(typeCast)
    bot_settings_dict[key] = typeCast(value)
    save_dictionary(filePath= PATH_BOT_SETTINGS_JSON,jsonString=json.dumps(bot_settings_dict,indent=4))

def get_bot_settings_keys():
    keys  = []
    
    for value in bot_settings_dict:
        if value[len(value)-2:] == "_C" or value[len(value)-2:] == "_T":
            continue
        keys.append(value)
    return keys

TIMEZONE = pytz.timezone(get("TIMEZONE")) 
def set_time_zone(zone):
    global TIMEZONE 
    TIMEZONE = pytz.timezone(zone=zone) 
    set(key="TIMEZONE",value=zone)
#endregion



#region === Init ===


def init():
    global PATH_XPATH_SETTINGS_JSON, PATH_BOT_SETTINGS_JSON,xpath_settings_dict,bot_settings_dict
    x = load_dictionary(PATH_XPATH_SETTINGS_JSON)
    if x != None:
        # if dictionary was loaded correctly,
        xpath_settings_dict =x
    else:
        # if dictionary was unable to load, save a new json
        save_dictionary( filePath= PATH_XPATH_SETTINGS_JSON,jsonString= json.dumps(xpath_settings_dict,indent=4))

    x = load_dictionary(PATH_BOT_SETTINGS_JSON)
    if x != None:
        # if dictionary was loaded correctly,
        bot_settings_dict =x
    else:
        # if dictionary was unable to load, save a new json
        save_dictionary( filePath= PATH_BOT_SETTINGS_JSON,jsonString= json.dumps(bot_settings_dict,indent=4))

init()
#endregion