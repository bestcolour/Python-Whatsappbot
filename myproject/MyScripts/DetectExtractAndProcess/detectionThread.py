'''
\nThis file holds the update loop for the all processes related to detection, extraction and processing of whatsapp messages on whatsapp web.
'''


import asyncio
# Common Managers
from MyScripts.threadmanager import thread_manager as _threadManager
from MyScripts.DetectExtractAndProcess.detectMsgFunctions import _find_msg_outside_group_ as _getNumOfUnreadMsg
# from MyScripts.DetectionAndExtraction.detectMsgFunctions import _find_msg_outside_group_ as _getNumOfUnreadMsg, init_msg_functions as _initMsgFunc
from .msgExtractionFunc import extractUnreadMessages as _extractMsg
from .processMgsFunctions import process_msg , init_process_msg

DETECT_THREAD_UPDATE_INTERVAL = 1


def detect_thread_init():
    init_process_msg()


async def detection_and_extraction_update():
    """
    \nThe update loop for detecting, extracting and processing whatsapp messages.
    \nThe function manages itself on the threadmanager's web queue by checking if it is queued and queues if it has not.
    \nOnly when it is this thread's turn does the detection and extraction processes run.
    """
    x = -1
    webThreadUserEnum =  _threadManager.WebThreadUsers
    isQueued = False

    while(_threadManager.get_StopThreadFlag() == False):
        #region === Web Queue ===
        if(isQueued is False):
            isQueued = True
            _threadManager.queue_in_web_queue(webThreadUserEnum.DETECT_AND_PROCESS)
            await asyncio.sleep(DETECT_THREAD_UPDATE_INTERVAL)
            continue


        # if current web queue is not this thread,
        if(_threadManager.get_curr_in_web_queue() != webThreadUserEnum.DETECT_AND_PROCESS):
            await asyncio.sleep(DETECT_THREAD_UPDATE_INTERVAL)
            continue
        #endregion
        

        x = _getNumOfUnreadMsg()
        if(x > 0):
            process_msg(_extractMsg(x))
            

        #reset
        isQueued = False
        _threadManager.pop_web_queue()
        await asyncio.sleep(DETECT_THREAD_UPDATE_INTERVAL)


