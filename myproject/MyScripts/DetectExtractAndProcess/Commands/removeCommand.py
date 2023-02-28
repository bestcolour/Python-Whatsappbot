from .baseBotCommand import baseBotCmd
from MyScripts.Background.backgroundThread import remove_on_going_command
from ..clickerFunctions import type_and_send_convo_input

class removeCommand(baseBotCmd):
    '''
    Removes an ongoing command using the ID the user has given. Is an instant command.
    '''
    def __init__(self, groupChatName, msg,loadedJsonData=None,isLoadingFromJSON = False):
        super().__init__(groupChatName, msg,loadedJsonData,isLoadingFromJSON)
        self.isInstant = True
        splitMsg = msg.split()
        try:
            # use the 2nd element index to remove the cmd
            remove_on_going_command(commandID = splitMsg[1],groupChatName= groupChatName)
            type_and_send_convo_input("Successfully removed command with the id '{}'".format(splitMsg[1]))
        except:
            raise ValueError("Command ID for removal is incorrect")
        
        


    # since this command is instant we dont need to write anything for the abstract methods below
    def update(self):
        return True
    