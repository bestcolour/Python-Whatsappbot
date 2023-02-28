from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch the web driver and go to the WhatsApp web page
driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com/')

# Wait for the user to log in and scan the QR code
input('Press Enter once you have logged in and scanned the QR code')

# Start an infinite loop to check for new messages
while True:
    # Find the latest message element on the page
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@data-testid='icon-unread-count']"))
        )
        
        if(element != None):
            # Print the latest message
            print("New message detected!")
            break
        
    except:
        # If no new messages are found, do nothing
        pass