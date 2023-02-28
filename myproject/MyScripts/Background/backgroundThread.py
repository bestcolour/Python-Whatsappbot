# This file holds code to only start and stop the thread for input. It doesnt hold any input code at all
# This is like a secondary thread that handles the input aspect of the program.
# It will gather input and then queue an order to the background processing thread to handle the order
# import threading
import asyncio
# Common Managers
from MyScripts.threadmanager import thread_manager as _threadManager
from MyScripts.botEvents import sub_to_on_msg_processed_done as _subMsgProcessDone, unsub_from_msg_processed_done as _unsubMsgProcessDone
import json
import MyScripts.saveLoadManager as saveLoadManager
import settings

THREAD_UPDATE_INTERVAL = 1
savetimer = 0

_ongoing_commands = {}
'''
\nA dictionary that holds all of the command instances that are running in the background thread.
\nKey: Group chat name. Value: Dictionary (Key: Unique ID of the command instance. Value: The command instance)
'''
_toberemoved_commands = []
'''
\nA list that holds all of the command instances that are about to be removed in the next cycle of the background thread updating.
'''

# region ===== Event Handling =====
def handle_msg_processing_done(botCmdLists):
    '''
    \nAdds new command instances into the on going commands collection to update
    '''
    global _ongoing_commands
    for i in range(len(botCmdLists)):
        cmdTask = botCmdLists[i]
        # get dictionary
        dictionary = _ongoing_commands.get(cmdTask.groupChatName,None)

        #if there is not dictionary, create one
        if dictionary is None:
            _ongoing_commands[cmdTask.groupChatName] = {}    
            dictionary = _ongoing_commands[cmdTask.groupChatName] 

        # add the cmd to the groupchat dictionary
        dictionary[cmdTask.id] = cmdTask


def handle_on_exit_():
    _unsubMsgProcessDone(handle_msg_processing_done)
    save_on_going_commands() # save everything b4 exiting
    _threadManager.unsubscribeToOnExit(handle_on_exit_)
# endregion


def bg_thread_init():
    _subMsgProcessDone(handle_msg_processing_done)
    _threadManager.subscribeToOnExit(handle_on_exit_)


async def bg_thread_update():
    """
    Updates any commands that has been sent by the extraction thread.
    """
    global _ongoing_commands
    webThreadUserEnum = _threadManager.WebThreadUsers
    isQueued = False
    global _toberemoved_commands
    _toberemoved_commands = []
    global savetimer

    while (_threadManager.get_StopThreadFlag() == False):
        #region === Occasional Saving ===
        savetimer += THREAD_UPDATE_INTERVAL
        if savetimer >= settings.get("AUTO_SAVE_FREQUENCY"):
            save_on_going_commands()
        #endregion

        # region === Checking for Web Queue ===
        if (len(_ongoing_commands) <= 0):
            await asyncio.sleep(THREAD_UPDATE_INTERVAL)
            continue

        if (isQueued is False):
            isQueued = True
            _threadManager.queue_in_web_queue(webThreadUserEnum.BACKGROUND)
            await asyncio.sleep(THREAD_UPDATE_INTERVAL)
            continue

        # if current web queue is not this thread,
        if (_threadManager.get_curr_in_web_queue() is not webThreadUserEnum.BACKGROUND):
            await asyncio.sleep(THREAD_UPDATE_INTERVAL)
            continue
        # endregion

        # update all command instances only when it is background thread's turn
        # for every dictionary in the ongoing command dictionary
        for dictionary in _ongoing_commands:
            dictionary = _ongoing_commands[dictionary]
            for cmdInstance in dictionary:
                cmdInstance = dictionary[cmdInstance]
                # update command instance, if it returns true that means command is done updating
                try:
                    if (cmdInstance.update() is True):
                        # remove the instance
                        _toberemoved_commands.append(cmdInstance)
                except:
                    print("Unable to update the cmdInstance:\n{}".format(cmdInstance.id))
        # remove if there is any to remove
        for cmdInstance in _toberemoved_commands:
            dictionary = _ongoing_commands[cmdInstance.groupChatName] # the dictionary that holds key as id and value as cmd instance
            dictionary.pop(cmdInstance.id)# remove the cmd instance 

            # check if dictionary is empty. If it is, then remove the dictionary from _ongoing_commands
            if len(dictionary) == 0:
                _ongoing_commands.pop(cmdInstance.groupChatName)

            print("The command instance with the id '{}' has been removed.".format(cmdInstance.id))

            # _ongoing_commands.pop(_toberemoved_commands[dictionary].id)
            # print("The command instance with the id '{}' has been removed.".format(
                # _toberemoved_commands[dictionary].id))

        # reset
        if len(_toberemoved_commands) > 0:
            _toberemoved_commands.clear()
            if settings.get("SAVE_WHENVER_A_COMMAND_HAS_BEEN_COMPLETED") == 1:
                save_on_going_commands() # save whenever 1 cmd is cleared is gone

        isQueued = False
        _threadManager.pop_web_queue()
        await asyncio.sleep(THREAD_UPDATE_INTERVAL)

#region ===== Methods For Bot Cmd =====
#region ----- Get On Going Commands Print -----
def get_on_going_commands_in_groupchat_as_string(groupChatName):
    '''
    \nReturns a string displaying all the ongoing command instances in the background thread that belong to the group chat given in as an argument.
    '''
    global _ongoing_commands
    index = 0
    string = []
    string.append("\n===== On Going Commands =====\n Index |  Message  |  ID  |\n")

    dictionary = _ongoing_commands.get(groupChatName)
    # only append if there is a dictionary to do so else
    if dictionary is not None: 
        for id in dictionary:
            string.append("\n{} | {} | {}".format(index,  dictionary[id].msg, id))
            index += 1

    string = "".join(string)
    return string

def get_all_on_going_commands_as_string():
    '''
    \nReturns a string displaying all the ongoing command instances in the background thread.
    '''
    global _ongoing_commands
    index = 0
    string = []
    string.append("\n===== On Going Commands =====\n Index |  Message  |  ID  |\n")

    # if there is no group chat as an arguement, print all of the on going commands from all group chats
    for groupChatName in _ongoing_commands:
        string.append("\n----- {} -----".format(groupChatName))
        dictionary = _ongoing_commands[groupChatName]
        for id in dictionary:
            string.append("\n{} | {} | {}".format(index,  dictionary[id].msg, id))
            index += 1

    string = "".join(string)
    return string


def print_on_going_commands():
    print(get_all_on_going_commands_as_string())
#endregion

def remove_on_going_command(commandID, groupChatName = None):
    global _ongoing_commands
    global _toberemoved_commands

   
    try:
        #if group chat name is not given, we have to find it ourselves in a time complexity of o(n)
        if groupChatName is None:
            for groupChatName in _ongoing_commands:
                dictionary= _ongoing_commands[groupChatName]

                # see if the id belongs to this dictionary
                instance =  dictionary.get(commandID)
                # if groupchat exists
                if instance is not None:
                    _toberemoved_commands.append(instance)
                    break
        # else, just get the instance
        else:
            # else if the instance exists
            dictionary = _ongoing_commands[groupChatName]
            instance = dictionary.get(commandID)
            assert (instance is not None)
            _toberemoved_commands.append(instance)
    except:
        print("There is no on going command with the id '{}' and hence no command instance will not be removed.".format(commandID))
        raise ValueError("None cannot be appended to _toberemoved_commands")

#region ----- Saving Methods -----
def save_on_going_commands():
    '''
    \nSaves all of the on going commands' data into a json file.
    '''
    jsonString = _get_json_of_commands_()
    saveLoadManager.save_to_data_file(jsonString)
    global savetimer 
    savetimer = 0
    print("=== Finished Saving OnGoing Commands ===")



def _get_json_of_commands_():
    '''
    \nReturns a string of all ongoing json commands saved in json format
    '''
    global _ongoing_commands
    #final dictionary is gunna look like this:
    # finalDictionary = {
    #       "GroupchatName1" : [jsonData1,jsonData2,jsonData3]
    #       "GroupchatName2" : [jsonData1,jsonData2,jsonData3]
    #       "GroupchatName3" : [jsonData1,jsonData2,jsonData3]
    # }
    finalDictionary = {}
    
    for groupChatDictionary in _ongoing_commands:
        groupChatDictionary = _ongoing_commands[groupChatDictionary]
        for cmdInstance in groupChatDictionary:
            cmdInstance= groupChatDictionary[cmdInstance]
            dataDict = cmdInstance.save_as_dictionary()
            # save json data into finaldictionary's dictionaries 

            # if there is no such group chat list alrdy existing,
            if finalDictionary.get(cmdInstance.groupChatName) is None:
                finalDictionary[cmdInstance.groupChatName] = []

            # add the data into the group chat list
            finalDictionary[cmdInstance.groupChatName].append(dataDict)
    
    return json.dumps(finalDictionary,indent=4)

#endregion
#endregion
