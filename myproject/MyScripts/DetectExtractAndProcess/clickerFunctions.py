'''
\nThis file holds the functions responsible for finding certain whatsapp web elements and acting in them.
'''

# region ===== Selenium Imports =====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# endregion

import pyperclip

from MyScripts.driverManager import driver_manager as _driverManager
import settings

def get_focused_groupchat_title():
    '''
    \nGetting the currently focused group chat on whatsapp web. 
    '''
    try:
        return _driverManager.get_driver().find_element(By.XPATH,settings.get("XPATH_GROUPCHAT_TITLE")).text
    except:
        print("Group chat title not found!")
        return None

def _find_input_field_bar_():
    '''
    \nFinds and clicks on the input field bar to reply a message. Returns the field bar element.
    '''
    driver = _driverManager.get_driver()
    inputField = driver.find_element(
        By.XPATH, settings.get("XPATH_MESSAGE_INPUT_FIELD"))
    # inputField =  inputField.find_element(By.XPATH, "./*")
    inputField.click()
    return inputField


def type_and_send_convo_input(msg):
    '''
    \nFinds and types into the conversation input field your msg and press Enter key to send the message. Returns the convo input element.
    '''
    try:
        fieldBarElmt = _find_input_field_bar_()
    except:
        print("Unable to find convo input bar!")
        raise AssertionError
    # i wanna make sure that my original clipboard data (if any) remains after this short transaction of control over the clipboard
    prevText = pyperclip.paste()
    pyperclip.copy(msg)
    
    myAction  = ActionChains(_driverManager.get_driver())
    myAction.key_down(Keys.CONTROL )
    myAction.send_keys("V")
    myAction.key_up(Keys.CONTROL)
    myAction.pause(settings.get("CONVO_INPUT_PAUSE"))
    myAction.send_keys(Keys.ENTER )
    myAction.perform()
    pyperclip.copy(prevText)
    
    # for i in range(len(msg)):
        # fieldBarElmt.send_keys(msg[i])
    # fieldBarElmt.send_keys(Keys.ENTER)
    # fieldBarElmt.send_keys(Keys.CONTROL + "V")
    # fieldBarElmt.send_keys(Keys.ENTER)
    return fieldBarElmt

def return_to_default_group():
    '''
    \nExits out of any focused whatsapp web group chat by pressing 'esc'.
    \nIs the replacement for enter_group_chat("Default")
    '''
    action = ActionChains(driver=_driverManager.get_driver())
    action.send_keys(Keys.ESCAPE)
    action.perform()


def enter_group_chat(grpChatName):
    '''
    \nClicks on the group chat search bar and searches for the group you want before clicking and entering into it
    '''

    driver = _driverManager.get_driver()
    try:
        # search_box = driver.find_element(By.XPATH, settings.XPATH_GROUP_SEARCH_BOX)
        search_box = driver.find_element(By.XPATH, settings.get("XPATH_GROUP_SEARCH_BOX"))
    except:
        print("Unable to find chatgroup search bar")
        raise AssertionError

    #region --- Entering GroupName into Searchbar ---
    search_box.click()

    #store prev text and then copy the grpchatname into clipboard
    prevClipboard = pyperclip.paste()
    pyperclip.copy(grpChatName)
    
    #paste the text into the group search bar
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL)
    action.send_keys("V")
    action.key_up(Keys.CONTROL)
    action.perform()

    pyperclip.copy(prevClipboard)
    #endregion

    try:
        # this will find the group with the exact text for sure
        groupChatElmt = driver.find_element(By.XPATH, settings.get("XPATH_MATCHED_TEXT").format(grpChatName))
            
        action = ActionChains(driver)
        action.pause(settings.get("GROUPCHAT_SEARCH_PAUSE"))
        action.click(groupChatElmt)
        action.perform()
    except:
        print("Unable to find group chat: '{}'".format(grpChatName))

        # only return value error if it is a phone number
        # code will be unable to find matched text only if the phone number is not exactly the same (whitespace sensitive)
        if grpChatName[0] == '+' or grpChatName.isdigit():
            print("Phone number may be the first time the bot is messaging or it did not have the correct spacing between the digits!")
            raise ValueError
        
        raise AssertionError
        
    finally:
        # search_box.click()
        # search_box.clear()
        # we must use crlt a + backspace because this will set the ui back to normal and we can view all the group conversations in the list (for detecting new unread)
        search_box.send_keys(Keys.CONTROL, 'a')
        search_box.send_keys(Keys.BACK_SPACE)
    

def start_convo_with_new_num(phoneNum):
    '''
    Starts a conversation by opening 'https://wa.me/+phoneNum' in the driver as a new tab. Then, sets the input field bar on focus.
    '''
    driver = _driverManager.get_driver()

    # Construct the wa.me URL for the phone number by concatenating the phone number to the end of the URL. For example, if the phone number is 15551234567, the wa.me URL would be https://wa.me/15551234567.
    link = settings.get("LINK_START_CONVO_WITH_NEW_NUM") + phoneNum

    #open new tab
    driver.execute_script("window.open('{}');".format(link))
    driver.switch_to.window(driver.window_handles[1])

    #close old tab
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, settings.get("XPATH_CONTINUE_TO_CHAT_BUTTON"))))
    element.click()


    # create the href link that we are going to use to search for the hyperlink element
    # the hyperlink is the 2nd and last elemnt we need to press before we can reach the page where the conversation with the new number is loaded
    link = settings.get("XPATH_USE_WHATSAPP_WEB_HYPERLINK").format(phoneNum )

    # we are finding a html block with the unique id. This html is the parent of the hyperlink we are looking for
    element = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located(
    (By.ID,settings.get("ID_FALLBACK_BLOCK"))))

    element =  element.find_element(By.XPATH,link)

    # click the final element to reach our conversation
    element.click()

    #now we wait until the page is loaded before letting the code flow
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, settings.get("XPATH_MESSAGE_INPUT_FIELD"))))
    


