from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# note: If there is no new messages in the group, it takes about 25-30 seconds before the elmt child size increases on its own 


class custom_condition(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, parentElmt, prevChildLength):
    self.parentElmt = parentElmt
    self.prevChildLength = prevChildLength

  def __call__(self, driver):
     return len(self.parentElmt.find_elements(By.XPATH, "./*")) > self.prevChildLength

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

input("Press Enter to check for new unread messages within the group")


element = driver.find_element(
    By.XPATH, "//div[@role='application']")  # parent element
# return direct children of the parent element
children_Elmts = element.find_elements(By.XPATH, "./*")
prevChildLength = len(children_Elmts)
# Start an infinite loop to check for new messages
print("prevChildLength = {}".format(prevChildLength))
while True:
    # Find the latest message element on the page
    try:
        WebDriverWait(driver, 60).until(
            custom_condition(element,prevChildLength)
        )

        # Print the latest message
        print("New message detected!")
        print("Number of children {}".format(len(element.find_elements(By.XPATH, "./*"))))
        break

    except:
        # If no new messages are found, do nothing
        pass

input("Press Enter to exit")
# Close the driver
driver.quit()
