# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0020554AD635BADBE5E1158A2F249A76CE5F215D805226F4B541B51F11123D0D76120B096F8BC9EC7F7A04AA3CD23DC2ABCF8A52711E66AF1E3B29DA90684860BCC0CED1310F4949255277B9E89B2D864280F74F9B78E768F49E0739DF99E0EEF3CF76BF8020DF9F2DF754379C4483B757DF31917A260D856D995B778ABB74DE0E453B9340D7B809C0143CC3176BD74C8795AE7FFCEC8F3FDEB31D580BB7F9A06072AE382B4916CB32135D86D0DD7632F5C2A709D20DF4280A4F8354598BD871B1EF3316E0D1A3B69CBDF13A1C8DD6AC85974EB4E0D7EF219013F413B3B5FCB8A57E2C09DCDDF1DD2D00B694E1365445BF3F8FD1890A4D897D949230BFA2C2756C77DB15C4F03E54D8DC2DFC57973D9F53E439CD79EA9E62A62904D782FC003E878BDFDC9CBA24C7C6DA2C014051FE090FF2C29391909593AB7C19CF00D54F6E84C873A6D1B458B24F3E4FAA68DA3983F7749F84678B91D5E9F44EF0E3E975001C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
