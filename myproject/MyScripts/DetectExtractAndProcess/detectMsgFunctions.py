'''
\nThis file holds the functions that are used to detect messages and act upon detecting so.
'''

#region ===== Selenium Imports =====
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#endregion
import settings

from MyScripts.driverManager import driver_manager as _driverManager

def _click_groupchat_(unreadIconElement):
    '''
    \nClicks on the unread icon element that whatsapp shows when there is a new unread message at the group chat UI.
    '''
    driver = _driverManager.get_driver()
    action = ActionChains(driver=driver)
    action.move_to_element_with_offset(
        to_element=unreadIconElement, xoffset=-50, yoffset=0)
    action.click()
    action.perform()



def _find_msg_outside_group_():
    '''
    \nSearches for 'icon-unread-count' element that appears on any whatsapp group that the whatsapp app is not inside. Returns the number of unread messages at the point of reading that element text. Enters the group which the unread messages are located. 
    '''
    driver = _driverManager.get_driver()
    try:
        element = WebDriverWait(driver, 0.02).until(EC.visibility_of_element_located(
            (By.XPATH,settings.get("XPATH_UNREAD_MSG_ICON") )))
    except:
            return 0

    numOfUnreadMsg = int(element.text)
    print("New messages detected outside of group! Number of unread messages: {}".format(element.text))
    # click group chat to prep for extraction
    _click_groupchat_(element)

    return numOfUnreadMsg
