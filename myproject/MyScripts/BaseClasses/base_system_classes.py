from abc import ABC,abstractmethod
import time


class base_singleton(ABC):
    """
    A class that when inherited, could be used to return a static instance of itself.
    """

    #------------- Begin Singleton Initialization -----------------
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance: # if static class instance is null/none
            cls._instance = super(base_singleton, cls).__new__(cls, *args, **kwargs) #assign this instance
        return cls._instance

    @classmethod
    def get_static_instance(cls):
        return cls._instance
    #------------- End Singleton Initialization -----------------



class base_proxymanager(ABC):
    """
    A manager class which requires other sources to update it and call its functions
    """

    #------------- Begin Singleton Initialization -----------------
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:# if static class instance is null/none
            cls._instance = super(base_proxymanager, cls).__new__(cls, *args, **kwargs)#assign this instance
        return cls._instance

    @classmethod
    def get_static_instance(cls):
        return cls._instance
    #------------- End Singleton Initialization -----------------

    def __updateLoop__(self):
        """
        The code which will be called by an outside entity every interval (determined by the passed in value in the constructor )
        Holds code which checks the current time to see if it has reached or passed the planned nextUpdateTime. If it has, __update__() will be called
        """
        #If current time is not passed nextUpdate time, return
        currentTime = time.time()
        if(currentTime < self.nextUpdateTime):
            return

        #Call update
        self.nextUpdateTime = currentTime + self.updateInterval
        self.__update__()


    @abstractmethod
    def __update__(self):
        """
        The code ran during every update interval.
        """
        pass


    def __init__(self, updateInterval=0.02):
        """
        Stores the updateInterval in self and checks every time __update__ is called whether updateInterval's value has passed since the last update
        """
        self.updateInterval= updateInterval
        self.nextUpdateTime = time.time() + updateInterval

