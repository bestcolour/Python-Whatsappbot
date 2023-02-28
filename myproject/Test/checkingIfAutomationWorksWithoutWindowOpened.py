from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox()
driver.get("https://web.whatsapp.com/")


input("Scan the QR code and then press Enter")

# minimise the browser window
driver.minimize_window()

try:
    element = driver.find_element(By.XPATH, "//span[@data-testid='icon-unread-count']")
except:
    print("NoSuchElementException")

action = ActionChains(driver= driver)
action.move_to_element_with_offset(to_element=element,xoffset=-50,yoffset=0)
action.click()
action.perform()


input("Press Enter to exit")

# Close the driver
driver.quit()
