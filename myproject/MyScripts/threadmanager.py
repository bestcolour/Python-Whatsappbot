import events
from enum import Enum
from MyScripts.BaseClasses.base_system_classes import base_singleton as _base_singleton

class thread_manager (_base_singleton):
    """
    \nA class with a static instance that holds an event will be raised when the program exits.
    \nThis class also holds a web queue list that dictates which asyncio thread can run at the current time.
    \nThis is to prevent 2 threads running at the same time when both threads are running functions that clicks on web elements and performing actions like typing.
    """
    class WebThreadUsers (Enum):
        '''
        \nThe enum class that holds the name of each thread that wants to be in the web queue. 
        \nAdd to this enum if there are anymore asyncio threads that wants to join the web queue.
        '''
        BACKGROUND = 0
        DETECT_AND_PROCESS = 1

    def __init__(self):
        self._stopThreadFlag = False

        # Event is a void event
        self._eventsHolder_  = events.Events(("onExit", "OnFinishUsingWeb"))
        self._webQueueList = []
        
   

    @staticmethod
    def get_curr_in_web_queue():
        '''
        \nReturns an enum value that indicates which thread is currently using the web interface. If there is currently no threads using the webinterface, return none
        '''
        queueList = thread_manager._instance._webQueueList
        if(len(queueList) ==0):
            return None
        return queueList[0]
        

    @staticmethod
    def queue_in_web_queue(value:WebThreadUsers):
        '''
        \nQueues an enum value of the thread that wants to use the web interface.
        '''
        this = thread_manager._instance
        this._webQueueList.append(value)

    @staticmethod
    def pop_web_queue():
        '''
        \nRemoves the current web queue thread when the thread is done using the web interface
        '''
        this = thread_manager._instance
        this._webQueueList.pop(0)


    @staticmethod
    def get_StopThreadFlag():
        return thread_manager._instance._stopThreadFlag

    @staticmethod
    def set_StopThreadFlag(value):
        thread_manager._instance._stopThreadFlag = value     


    @staticmethod
    def subscribeToOnExit(function):
        """
        \nSubscribe to onExit event.
        """
        self = thread_manager._instance
        self._eventsHolder_.onExit += function

    @staticmethod
    def unsubscribeToOnExit(function):
        """
        \nUnSubscribe from onExit event.
        """
        self = thread_manager._instance
        self._eventsHolder_.onExit -= function

    @staticmethod
    def raiseOnExit():
        """
        \nCalls the onExit event
        """
        self = thread_manager._instance
        self.set_StopThreadFlag(True)
        self._eventsHolder_.onExit()
        print("====== Program End ======")
        #cannot call sys.exit else all of the threads will close by itself without having a controlled exit
        # sys.exit()

thread_manager() #instance itself