from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# initialize the webdriver
driver = webdriver.Firefox()

# navigate to the desired URL in the first tab
driver.get("https://www.google.com")

# switch to the first tab
main_tab = driver.current_window_handle

# open a new tab using the keyboard shortcut
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).key_down('t').key_up('t').key_up(Keys.CONTROL).perform()

input("enter to continue")
# switch to the new tab
new_tab = [tab for tab in driver.window_handles if tab != main_tab][0]
driver.switch_to.window(new_tab)

# navigate to the desired URL in the new tab
driver.get("https://www.python.org")

input("enter to continue")

# close the new tab and switch back to the main tab
driver.close()
driver.switch_to.window(main_tab)

# close the driver
driver.quit()
