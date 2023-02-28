# region ===== Selenium Imports =====
from selenium.webdriver.common.by import By
# endregion

from MyScripts.driverManager import driver_manager as _driverManager
from .botCommandsLibrary import check_if_is_command as _checkIsCmd, get_command as _getCmd, load_command as _loadCmd
from MyScripts.botEvents import raise_on_msg_processed_done as _raiseMsgProcessed
from .clickerFunctions import type_and_send_convo_input , return_to_default_group
import MyScripts.saveLoadManager as saveLoadManager
# import json
import settings

def init_process_msg():
    '''
    \nChecks for any command instances to load from the data.json file
    '''
    finalDictionary = saveLoadManager.read_from_data_file()


    # if there is nothing to load,
    if finalDictionary is  None:    
        return

    loadedInstaces =[]
    print("--- Loading Saved Commands ---".format())
    for groupChatList in finalDictionary:
        groupChatList = finalDictionary[groupChatList]
        for cmdInstanceDataDict in groupChatList:
            # load a new cmd instance using data and add it to list
            cmdInstanceDataDict = _loadCmd(cmdInstanceDataDict)
            #if there is error with loading the cmd instance, dont add it to list
            if cmdInstanceDataDict is None:
                continue

            loadedInstaces.append(cmdInstanceDataDict)

    #send the list to background thread
    _raiseMsgProcessed(loadedInstaces)


#region === Processing Messages ===
def process_msg(checkedRowElmts):
    '''
    \nChecks through all the messages to see if there are any bot commands.
    \nIf there are any non-instant bot commands, replies to that specific message as a acknowledgement.
    \nThe processed messages are messages with valid bot commands in it. They will be sent to the background thread for updating via raising the on_message_processed event in the botEvents.py
    \nWill return the whatsapp focused chat group to default after raising the event.
    '''
    cmdInstances = []
    messages = []
    # timeStamps = []
    currentGroupChatName = _driverManager.get_driver().find_element(By.XPATH,settings.get("XPATH_GROUPCHAT_TITLE")).text

    #extract messages and time
    for i in range(len(checkedRowElmts)):
        rowElmt = checkedRowElmts[i]
        try:
            # settings.XPATH_MESSAGE_TEXT replace here
            msgElmt = rowElmt.find_element(
                By.XPATH, ".//span[@class='_11JPr selectable-text copyable-text']")
            messages.append(msgElmt.text)

        except:
            print("No message element found!")


        # try:
        #     timeElmt = rowElmt.find_element(
        #         By.XPATH, settings.XPATH_MESSAGE_TIME)
        #     timeStamps.append(timeElmt.text)

        # except:
        #     print("No time element found!")

    print("Extracted the messages:")
    print(messages)
    # print("Extracted the timestamps:")
    # print(timeStamps)

    for i in range(len(messages)):
        if ( _checkIsCmd(messages[i]) is False):
            continue

        # if it is a bot command,
        # reply to that message element and acknowledge it 

        # instantiate cmdInstance and add it into the cmd
        cmdInstance = _getCmd(currentGroupChatName,messages[i])
        if(cmdInstance is  None):
            continue
        
        cmdInstances.append(cmdInstance)
        #region --- Acknowledgement Message ---
        if not cmdInstance.isInstant:
            thingToType = "Acknowledged your request '{}'.\nThe id for your command is:".format(messages[i])
            type_and_send_convo_input(thingToType)
            thingToType = cmdInstance.id
            type_and_send_convo_input(thingToType)
        #endregion
        

    # finally send this list to the background thread to update
    _raiseMsgProcessed(cmdInstances)
    return_to_default_group()
#endregion
