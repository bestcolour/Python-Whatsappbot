from MyScripts.threadmanager import thread_manager as _thread_manager
from MyScripts.driverManager import driver_manager
from MyScripts.Background.backgroundThread import remove_on_going_command, save_on_going_commands as save
import os
from MyScripts.botEvents import raise_on_msg_processed_done as _raiseMsgProcessed
from MyScripts.DetectExtractAndProcess.botCommandsLibrary import get_command, check_if_is_command
import settings
import phonenumbers
import pytz

def exit_program():
    '''To call this command type 'exit'
    \nExits the console and closes the browser properly.
    '''
    _thread_manager.raiseOnExit()
    exit()

def refresh_driver():
    '''To call this command type 'refresh'
    \nRefreshes the browser.
    '''
    print("Refreshing driver...")
    driver_manager.refresh_driver()
    print("Driver refreshed")
    

def remove_command():
    '''To call this command type 'remove og'
    \nAsks the user on the console for an input. The input ought to be an ID that belongs to one of the on going commands running on the background thread. If ID is correct, that command instance will be removed.
    '''
    userInput = input("\nPlease give the ID of the command instance you want to remove:\n")
    remove_on_going_command(userInput)

def print_help():
    '''
    To call this command type 'help'
    \nPrints the commands available in the console. 
    '''
    string = "\n\n===== Console Help ====="
    string += "\nBelow is a list of commands that you can run in this console."
    string += "\n- print og"
    string += "\n Prints all of the currently on going command instances on the console."
    string += "\n\n- refresh"
    string += "\n Refreshes the browser."
    string += "\n\n- remove og"
    string += "\n Clears the console text."
    string += "\n\n- send"
    string += "\n Sends a message to the given groupchat."
    string += "\n\n- save og"
    string += "\n Saves all of the ongoing command instances into a json file."
    string += "\n\n- clear"
    string += "\n Removes an on going command instance by inputing its respective ID."
    string += "\n\n- settings"
    string += "\n Changes the bot settings."
    string += "\n\n- exit"
    string += "\n Exits the console and closes the browser properly."
    # "\n\n----- Mandatory KeyWords -----\nsend keyword: Must be the first keyword in the command. Phone number without +<num> will be treated as the same country code as the bot\n\nat keyword: time can be 24hr format or 12 hr format with '11.30pm' or '11.30 pm' accepted\n\nsemicolon keyword: Must be the last keyword in the command. Contains the message you want to send to the number.\n\n----- Optional KeyWords -----\non keyword: the date in which the message is to be sent. Must be in <day><month><year> format\n\nevery keyword: the interval in which the message is to be sent. Duration can be expressed in days (using the short form of 'd'), hours (h), minutes (m) and seconds (s)"
    print(string)


def save_on_going_commands():
    '''
    To call this command type 'save og'
    \nSaves all on going commands in the background thread.
    '''
    try:
        save()
    except:
        print("Something went wrong with saving!")
    pass

def clear_console():
    '''
    \nClears the console
    '''
    os.system('cls')

def sendmsg():
    '''
    \nCommands the bot to send a message. The parameters will be the same with how it works on whatsapp web.
    '''
    groupChatName = input("\nWhere do you want the message to be sent? (Groupchat name, phone number or a contact)")
    userInput = input("\nInput send message command (eg: 'send msg:lalalalal')")
    
    # make sure there is 
    if userInput[0] != '~':
        userInput = '~' +userInput

    if not check_if_is_command(userInput):
        print("Unable to send message! The given input is not in the send message command format!")
        return 

    # if userInput.find('to') == -1:
    #     print("You can't send message because there is no 'to' keyword in the input!")
    #     return
    
    instance = get_command(groupChatName= groupChatName,msg= userInput)
    if instance is None:
        return

    _raiseMsgProcessed([instance])

def change_settings():
    string = "=== Bot Settings ==="
    options = settings.get_bot_settings_keys()
    length = len(options)
    for i in range(length):
        #make the options look more appealing
        #use index to store the keys
        index  = options[i].replace("_"," ")
        index= index.lower().capitalize()

        string+="\n{}){}".format(i+1,index)
    print(string)
    index = input("Choose the setting you wish to change:\n")
    try:
        index= int(index)
        assert(index> 0 and index <= length)
        index -=1
    except AssertionError:
        print("Invalid number was given!\n")
        return
    except ValueError:
        print("The input you have given is not a whole number\n")
        return
    
    # print out the option's description
    key = options[index]
    description = settings.get(key+"_C")
    currVal = settings.get(key)
    if key == "ADMIN_NUMBERS":
        currVal = ", ".join(currVal)
        currVal = currVal.replace("'","").replace("[","").replace("]","")

    print("\n\n--- {key} ---\n{description}\n\nCurrent Value: {currVal}".format(key = key,description = description,currVal = currVal))

    # get new value and set it
    index = input("Please key in your new value:\n")
    try:
        match key:
            case "TIMEZONE":
                settings.set_time_zone(index)
            case "ADMIN_NUMBERS":       
                if bool(index) == True:
                    index = index.split(",")
                    for i in range(len(index)):
                        index[i] = phonenumbers.parse(index[i] , None)
                        index[i] = phonenumbers.format_number(index[i], phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                else:
                    index = []
                settings.set(key= key,value= index)
            case _:
                settings.set(key= key,value= index)

        print("Settings changed.")
    except pytz.UnknownTimeZoneError:
        print("Unable to change timezone to your inputed value as such timezone does not exist.\nVisit https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 to see the list of available timezones")
    except:
        print("Unable to change settings to that value. Please try again.")
