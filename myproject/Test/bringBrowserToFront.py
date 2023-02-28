#This code only selects the tab to be focused
# it doesnt bring the browser window to the front of the application window order

from selenium import webdriver

driver = webdriver.Firefox()

input("Set window to background then press Enter")

driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()

input("Press Enter to exit")

# Close the driver
driver.quit()