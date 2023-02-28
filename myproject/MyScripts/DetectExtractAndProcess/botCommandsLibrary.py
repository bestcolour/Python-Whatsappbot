'''
\nFile that contains the bot command library. Add to this file if you wish to add more bot commands. 
\nThe bot command identifier is also defined here.
'''

# region ===== Command Imports =====
from .Commands.helpCommands import help
from .clickerFunctions import type_and_send_convo_input
from .Commands.SendMessage.sendMessageCommands import sendMessageToGroup
from .Commands.removeCommand import removeCommand
from .Commands.listCommand import listOnGoing_Command as listOnGoingCmd
# endregion
COMMAND_IDENTIFIER = '~'

command_library = {
    COMMAND_IDENTIFIER+"help": help,
    COMMAND_IDENTIFIER+"send": sendMessageToGroup,
    COMMAND_IDENTIFIER+"remove": removeCommand,
    COMMAND_IDENTIFIER+"list":listOnGoingCmd
}


def check_if_is_command(message):
    '''
    \nChecks if the inputed message has the command identifier as its first character
    '''
    if (message[0] == COMMAND_IDENTIFIER):
        return True
    return False


def get_command(groupChatName,msg):
    '''
    \nRead the msg and check if there are the correct keywords in it. If so, then instantiates a base task class and returns it.
    '''
    # find the first word of the msg 
    cmdType = []
    for char in msg:
        if char == ' ':
            break
        cmdType.append(char)
    
    cmdType = "".join(cmdType)
    cmd = command_library.get(cmdType)

    # command type is found in the command library
    if(cmd is not None):
        try: 
            cmd = cmd(groupChatName,msg)
            return cmd  
        except:
            unrecognizedCmd_msg = "The command you tried to call ({}) was not successful. Please check that you have followed the correct format to using it".format(cmdType)
            print(unrecognizedCmd_msg)
            type_and_send_convo_input(unrecognizedCmd_msg)
            return None
    else:
        unrecognizedCmd_msg = "\nUnable to find the command '{}'. Type {}help for more information".format(cmdType,COMMAND_IDENTIFIER)
        print(unrecognizedCmd_msg)
        type_and_send_convo_input(unrecognizedCmd_msg)
        return None

def load_command(cmdDataDict):
    '''
    \nLoads a command instance using json data. Returns the instantiated command.
    '''
    # find the first word of the msg 
    cmdType = []
    for char in cmdDataDict["msg"]:
        if char == ' ':
            break
        cmdType.append(char)
    
    cmdType = "".join(cmdType)
    cmd = command_library.get(cmdType)

    # command type is found in the command library
    if(cmd is not None):
        try: 
            cmd = cmd(None,None,loadedJsonData = cmdDataDict,isLoadingFromJSON = True )
            unrecognizedCmd_msg = "\nSuccessfully loaded the previously saved command:\nType: {}\nid: {}\ngroupChatName: {}\nmsg: {}".format(cmdType,cmdDataDict["id"],cmdDataDict["groupChatName"],cmdDataDict["msg"])
            print(unrecognizedCmd_msg)
            return cmd  
        except:
            unrecognizedCmd_msg = "Unable to load the previously saved command:\nType: {}\nid: {}\ngroupChatName: {}\nmsg: {}".format(cmdType,cmdDataDict["id"],cmdDataDict["groupChatName"],cmdDataDict["msg"])
            print(unrecognizedCmd_msg)
            return None
    else:
        unrecognizedCmd_msg = "\nUnable to find and load the command type '{}'. Type {}help for more information\nData Dict: \n{}".format(cmdType,COMMAND_IDENTIFIER,cmdDataDict)
        print(unrecognizedCmd_msg)
        return None
