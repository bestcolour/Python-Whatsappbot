from .baseBotCommand import baseBotCmd
from ..clickerFunctions import type_and_send_convo_input

class help(baseBotCmd):
    '''
        Prints all the commands that the bot can do.
    ''' 
      
    def __init__(self, groupChatName, msg,loadedJsonData=None,isLoadingFromJSON = False):
        
        super().__init__(groupChatName, msg,loadedJsonData,isLoadingFromJSON)
        self.isInstant = True
        # Use selenium to access the input bar and type in the following message
        thingToType = "Here are the list of things you could do using this bot\n\n"
        thingToType += "*-> Send Message to Group Chat*\n"
        thingToType += "'~send to +65 9123 4567 msg:lalalalallala'\nThis will send the message to the phone number +65 9123 4567\n"
        thingToType += "\n'~send at 11.59 pm on 160223 every 2d 2h 4m msg:lalalalallala'\nThis will send the message at 11.59pm on 16/02/2023 and then send the message every 2 days 2 hours and 4 minutes onwards"
        thingToType += "\n*-> Removing Pending Message*\n"
        thingToType += "\n'~remove aeN8rob9GjBNNxAxa9F3rr'"
        thingToType += "\n\n*-> Listing All Pending Messages*\n"
        thingToType += "'~list'"



        type_and_send_convo_input(thingToType)
        # print(thingToType)

    def update(self):
        return True
