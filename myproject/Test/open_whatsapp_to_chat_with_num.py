


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch the web driver and go to the WhatsApp web page
driver = webdriver.Firefox()
driver.get('https://wa.me/phonenumber')

# Wait for the user to log in and scan the QR code
input('Press Enter once you have logged in and scanned the QR code')

driver.close()