import abc
import shortuuid
import json
class baseBotCmd(abc.ABC):

    def __init__(self,groupChatName,msg,loadedJsonData = None,isLoadingFromJSON = False):
        self.isInstant = True
        if not isLoadingFromJSON:
            self.groupChatName = groupChatName
            self.msg = msg
            '''
            \nRepresents the raw message that the user typed to call the command.
            '''
            self.id = shortuuid.uuid()
            '''
            \nDetermines whether or not the acknowledgement message will be printed after the command is called from whatsapp.
            '''
        else:
            self.groupChatName = loadedJsonData["groupChatName"]
            self.msg = loadedJsonData["msg"]
            self.id = loadedJsonData["id"]
        

    def save_as_dictionary(self):
        '''
        \nThis method is called to convert the data needed to instantiate this class into a json format. 
        '''
        x  = {
            "groupchatname" : self.groupChatName,
            "msg": self.msg,
            "id":self.id
        }
        return x
    
    @abc.abstractmethod
    def update(self):
        '''
        \nThis method is called to update the command instance within an update loop.
        '''
        return True
