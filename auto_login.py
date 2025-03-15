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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F965228614C94E4742C322A8B791C16A4479F8F95C9CC595629E57DD513BCE2621E960503CE8CCC7BD8FC4F4447FD06EF4503225B8C1DF3CA99D4666FF80FAD5E388B4D24567D3124BC26388CEFE80F1E59A33659016CD5BE75BA23023F0E4FD439CE01BED9E4E11CC808092028D16814F79D0B5FD6914825A72781889F4F7DE6164588A006A6B13E8D84F2AE38A83F73957088A9AC470648660DFC46932EF502EA635608A7B946510BF35EDB03C7457D8803DA29EFDE518CFBA360C53095CDF51B14D010A3843C3CAA7A8D95D43D6A0278D9E0F9FE0D40BE911AA0F0437CD7FD92DA9CF4F51F4B78DE74F87280BDC95B83C81A6874A22241726EDEE4BF4240B74611EE47757C1DA1A03CCA24337FF8E42EDC2E4071CF746ECF263C0AF9801038AB83A2A393471EDAF0B99E66E3B978C3AC71AF67C5889251269BAE4BB790BCF730ED287DCDC67203CFBE8ACEE831D8DC14AFA9A3BD39AEDDFABA002C7D99D63"})
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
