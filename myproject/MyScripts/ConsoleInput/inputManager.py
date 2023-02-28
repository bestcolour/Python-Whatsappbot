from MyScripts.BaseClasses.base_system_classes import base_proxymanager as _baseProxyManager
from .Commands.commandDictionary import command_Dictionary as _cDict 



class input_manager(_baseProxyManager):
    """
    Responsible for the requesting of of console input and the usage of that input.
    """

    def __init__(self):
        # since input() stops the flow of code, we dont need an update interval because the rate at which the user types an input IS the update interval
        _baseProxyManager.__init__(self, updateInterval=0)

    def __update__(self):
        userInput = input().lower().strip()
        # tries to get the console command from a dictionary and call it
        try: 
            cmd = _cDict.get(userInput)
            cmd()
        except:
            print("Console command not recognized. Try typing 'help' to learn more.")
            