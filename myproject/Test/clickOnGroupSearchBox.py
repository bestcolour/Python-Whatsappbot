from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import asyncio

async def main():
        
    # Create a new Chrome driver
    driver = webdriver.Firefox()

    # Navigate to the WhatsApp web interface
    driver.get("https://web.whatsapp.com/")

    # Wait for the user to scan the QR code
    input("Scan the QR code and press Enter")

    # Find the search box and input the name of the group you want to search for
    search_box = driver.find_element(By.XPATH,"//div[(@role= 'textbox')]")
    search_box.click()
    search_box.send_keys("Transfer" + Keys.ENTER)

    asyncio.sleep(1)

    groupChatElmt = driver.find_element(By.XPATH,"//div[(@data-testid='message-yourself-row')]")
    groupChatElmt.click()
    print("Clicked on {}".format(groupChatElmt.text))

    input("Enter to quit")
    # Close the driver
    driver.quit()


asyncio.run(main())