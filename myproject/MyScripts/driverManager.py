'''
\nIs the file that opens web whatsapp on a browser.
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from MyScripts.BaseClasses.base_system_classes import base_singleton as _base_singleton
from .threadmanager import thread_manager 
import settings

class driver_manager(_base_singleton):

    def _handle_on_exit_(self):
            self.driver.quit()
            thread_manager.unsubscribeToOnExit(self._handle_on_exit_)

    def __init__(self):
        
        # if settings.get("ENABLE_HEADLESS_MODE") is True:
        #     op = Options()
        #     op.add_argument("--headless")
        #     self.driver = webdriver.Firefox(options=op)
        # else:
        self.driver = webdriver.Firefox()

        self.driver.get(settings.get("LINK_WHATSAPP_WEBPAGE"))
        self.driver.maximize_window()

        #make sure
        # if settings.get("ENABLE_HEADLESS_MODE") is True:
            # self._get_QR_screenshot_()
        input('Press Enter once you have scanned the QR code. If the QR code does not work, please restart the program as the QR code might have expired')

        thread_manager.subscribeToOnExit(self._handle_on_exit_)

    def _get_QR_screenshot_(self):
        '''
        Will wait until the QR code shows on the web and then get a screenshot of the QR code. 
        '''
        wait = WebDriverWait(self.driver, 10)

        while True:
            wait.until(EC.presence_of_element_located((By.XPATH, settings.get("XPATH_QR_CODE_ELEMENT"))))
            break

        # take screenshot
        self.driver.save_full_page_screenshot("qrCode.png")











    @staticmethod
    def get_driver():
        return driver_manager._instance.driver
    
    
    @staticmethod
    def refresh_driver():
        driver = driver_manager._instance.driver
        #open new tab
        driver.execute_script("window.open('{}');".format(settings.LINK_WHATSAPP_WEBPAGE))
        #close old tab
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])





driver_manager()

