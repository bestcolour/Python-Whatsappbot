'''
\nThis file holds functions for extracting and processing unread messages from an focused whatsapp group. 
'''

# region ===== Selenium Imports =====
from selenium.webdriver.common.by import By
# endregion

from MyScripts.driverManager import driver_manager as _driverManager
# from .botCommandsLibrary import check_if_is_command as _checkIsCmd, get_command as _getCmd
from MyScripts.botEvents import raise_on_msg_processed_done as _raiseMsgProcessed
from .clickerFunctions import type_and_send_convo_input 
import settings


def extractUnreadMessages(numOfUnreadMsg):
    '''
    \nExtracts unread messages from the focused chat group. Returns the unread messages in a list.
    '''
    # async def extractUnreadMessages(numOfUnreadMsg):
    driver = _driverManager.get_driver()
    parentElmt = driver.find_element(
        By.XPATH, settings.get("XPATH_PARENT_OF_ROWS"))  # parent element
    # return direct children of the parent element
    children_Elmts = parentElmt.find_elements(By.XPATH, "./*")

    # Extract info from every unread message row element (some can have phone numbers because that message is not continued by the previous sender but instead a new sender)
    # We must make sure that the child element we are reading has the "role" of "row" because things like "Date" or "Add contact" are also considered a child in the parent element
    # Example:
    # msg 1
    # msg 2 [index 2]
    # today [index 1]
    # msg 3 [index 0]

    newestMsgElmtIndex = len(children_Elmts) - 1
    numOfProcessedMsg = 0
    # holds row elements that indeed have been checekd to contain messages
    checkedRowElmts = []

    while (numOfProcessedMsg < numOfUnreadMsg):
        child = children_Elmts[newestMsgElmtIndex-numOfProcessedMsg]

        # check if the child element is the row element that contains the text msg we want
        if (child.get_attribute("role") != "row"):
            numOfProcessedMsg += 1
            numOfUnreadMsg += 1
            continue

        checkedRowElmts.append(child)
        numOfProcessedMsg += 1

    checkedRowElmts.reverse()
    return checkedRowElmts
    # _process_msg_(checkedRowElmts)
    # return_to_default_group()
