from .baseBotCommand import baseBotCmd
from ..clickerFunctions import type_and_send_convo_input
from MyScripts.Background.backgroundThread import save_on_going_commands as save

class saveAllOnGoing_Command(baseBotCmd):
    '''
    \nSaves all of the on going commands into a data file so that if anything happens to the server, they can be loaded in agn. 
    \nIs not officially in the list of commands that users can use because they shouldnt need to do this.
    '''
    def __init__(self, groupChatName, msg,loadedJsonData = None,isLoadingFromJSON = False):
        super().__init__(groupChatName, msg,loadedJsonData,isLoadingFromJSON)
        self.isInstant = False
        try:
            type_and_send_convo_input("Saving data now...")
            save()
            type_and_send_convo_input("Data saved")
        except:
            raise Exception
        
        


    # since this command is instant we dont need to write anything for the abstract methods below
    def update(self):
        return True