'''
This file holds code to only start and stop the thread for input. It doesnt hold any input code at all
This is like a secondary thread that handles the input aspect of the program. 
It will gather input and then queue an order to the background processing thread to handle the order
'''
import threading

# Common Managers
from MyScripts.threadmanager import thread_manager as _threadManager
# Input Thread Managers
from .inputManager import input_manager as _input_manager_


def input_thread_start():
    '''
    Starts the input thread to check for inputs
    '''
    inputThread = threading.Thread(target=_update_)
    inputThread.start()


def _update_():
    """
    The input thread loop updates managers which require user inputing on a OS thread.
    """
    # Initializing the Managers
    inputManager = _input_manager_()

    #update loop
    while(_threadManager.get_StopThreadFlag() == False):
        inputManager.__updateLoop__()

