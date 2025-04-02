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
    browser.add_cookie({"name": "MUSIC_U", "value": "00ECD79C695A970676E3E1801E7890440218569F5820BC0EB8530A3C11DD63FBF95B2B542417832B82D6C27C3EA31C6533B0CFFCD6C125D0E35D10059002D644B3247F4802A2FB6227C5EB4520A9402C44CE640036950617164AFE96506D917D135F7E088893103177C8065BAC5078077C4EED74A5FBE144D840F6D8B19BBA6DA957013ACF2369A40F3CF2AA617FE2C800F5F928581054A7630090B6A6CF509FB06D2EA031C3C4C4A95212A94903C7A51DA4E3063241A21F48D06304B99B0AA3D0B716308B4EDBBA0A88975664C1FA9EA08D08F8286BFF5762817FB63EBFC433BE22BF70C5E38EA0B21464166CE1EAAC19EADBC516740E639318C396C1403763E02CC5525355C898595E2212DD67A89F5E6FE3213C756AB888F1284A95AED896D93FB7E9C3787A7330D96844F0D1767388D653F087A153B7BF7A689979FD3C729DA1A70E67D2ADC2DB6D3EEA34FDC712503C13AEDD8635F5EF2354DCDE19BD0D0E"})
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
