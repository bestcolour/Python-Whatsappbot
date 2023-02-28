# region ===== Selenium Imports =====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# endregion

# Construct the wa.me URL for the phone number by concatenating the phone number to the end of the URL. For example, if the phone number is 15551234567, the wa.me URL would be https://wa.me/15551234567.

driver = webdriver.Firefox()
#open whatsapp web first so that future open tabs dont need any qr code
link = "https://web.whatsapp.com/"
driver.get(link)
driver.maximize_window()


input("Press enter after scanning qr code")


# I can't seem to open the link "https://wa.me/<phoneNum>" without the code stopping at the driver.get(link) and not progressing past that
# therefore i use execute script to do so.
driver.execute_script("window.open('https://wa.me/6587533510');")
driver.switch_to.window(driver.window_handles[1])

phonenumber = "6587533510"
# driver.get(new_url)

# link = link+phoneNum + "&text&type=phone_number&app_absent=0"
# https://web.whatsapp.com/
# https://wa.me/15551234567
input("Press enter to continue code")

element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//a[@id='action-button']")))
element.click()

link = "https://web.whatsapp.com/send/?phone=" + phonenumber+ "&text&type=phone_number&app_absent=0"
fallBackBlockElmt = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located(
    (By.ID, "fallback_block")))

fallBackBlockElmt =  fallBackBlockElmt.find_element(By.XPATH,".//a[@href='{}']".format(link))

fallBackBlockElmt.click()

input("Enter to continue code")

driver.switch_to.window(driver.window_handles[0])
driver.close()
driver.switch_to.window(driver.window_handles[0])
input("Enter to quit")
driver.quit()
