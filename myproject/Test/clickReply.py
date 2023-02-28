from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")

input("Scan the QR code and then press Enter")

try:
    element = driver.find_element(
        By.XPATH, "//span[@data-testid='icon-unread-count']")
    numOfUnreadMsg = int(element.text)
    print("Number of unread messages: {}".format(element.text))
except:
    print("NoSuchElementException")

action = ActionChains(driver=driver)
action.move_to_element_with_offset(to_element=element, xoffset=-50, yoffset=0)
action.click()
action.perform()



element = driver.find_element(By.XPATH, "//div[@role='application']") # parent element
children_Elmts = element.find_elements(By.XPATH, "./*") # return direct children of the parent element


# Extract info from every unread message row element (some can have phone numbers because that message is not continued by the previous sender but instead a new sender)
# We must make sure that the child element we are reading has the "role" of "row" because things like "Date" or "Add contact" are also considered a child in the parent element
#Example:
# msg 1
# msg 2 [index 2]
# today [index 1]
# msg 3 [index 0]

newestMsgElmtIndex = len(children_Elmts) - 1
numOfProcessedMsg = 0
messages = []
XPATH_MESSAGE_TIME = "//div[@data-testid='msg-meta']"


while (numOfProcessedMsg < numOfUnreadMsg):
    child = children_Elmts[newestMsgElmtIndex-numOfProcessedMsg]

    # check if the child element is the row element that contains the text msg we want
    if (child.get_attribute("role") != "row"):
        numOfProcessedMsg += 1
        numOfUnreadMsg += 1
        continue

    # Get the phone number first to categorize the messages
    # try:
    #     phoneNumElmt = child.find_element(By.XPATH, ".//span[@class='p_If-']")
    #     print(phoneNumElmt.text)
    #     tempList.append(phoneNumElmt.text)
    # except:
    #     print("No phone number element found!")

    msgElmt = child.find_element(
        By.XPATH, ".//span[@class='_11JPr selectable-text copyable-text']")
    # print("Msg: {}\n Size: {}".format(msgElmt.text,msgElmt.size))
    timeElmt = child.find_element(By.XPATH, XPATH_MESSAGE_TIME)
    print("Msg: {}\n Time: {}".format(msgElmt.text,timeElmt.text))


    numOfProcessedMsg += 1

# messages.reverse()
# print(messages)

# Attribute for msg -> class="_11JPr selectable-text copyable-text"
# textElement =  child.find_element(By.XPATH,"//span[@dir='ltr']")
# Attribute for phone number -> class="p_If-"


input("Press Enter to exit")
# Close the driver
driver.quit()
