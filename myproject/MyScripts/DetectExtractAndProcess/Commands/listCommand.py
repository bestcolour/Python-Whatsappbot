from .baseBotCommand import baseBotCmd
from MyScripts.Background.backgroundThread import get_on_going_commands_in_groupchat_as_string as get_on_going_cmds
from ..clickerFunctions import type_and_send_convo_input

class listOnGoing_Command(baseBotCmd):
    '''
    \nTypes and sends all of the ongoing commands within that group chat. 
    \nIs an instant command
    '''
    def __init__(self, groupChatName, msg,loadedJsonData = None,isLoadingFromJSON = False):
        super().__init__(groupChatName, msg,loadedJsonData,isLoadingFromJSON)
        self.isInstant = True
        try:
            # use the 2nd element index to remove the cmd
            type_and_send_convo_input(get_on_going_cmds(groupChatName))
        except:
            raise Exception
        
        


    # since this command is instant we dont need to write anything for the abstract methods below
    def update(self):
        return True