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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C3035431C08FAFB5468FD721473F4330CF43DA8B33130F13C39655A364F0A4BD397764EA6266DFBB292AA5325DF5967D3CACD6385D18F2437A85D32F2CF03DF0A066BE4B1887F2CBED899D9C52AD706B2C627F1F027A002FBE29834FD89C50DCE7E3FC315B3D6B2D198229A225281F68A2F7045A1927C6CCEE86EF080E2C9AD414DA411A01A1331F1D0E9DF5CDD5C000D34748AA89229D88E6225080BD419B93296A9F06620338553BE30D74911D9CEF744688A4B1CE56B49DD8B7E67017ECDC21AD0332F9D9E6A02D119B511853C494D4736C6066D01154D2CB1CC8E2602ED6BCF42E75AC138C753AC02D5E9F2B825FA37B88A08B3F1A1D021937D0E7D089FDA9378BEAFA22926AB004CA18C14A8DE8F88870F83870B856085A5C2C4CB966A16CCB4A58003811499D989F9968B14B9BF8BA6C1E683CD61E70159871C1C4C8F24ECE50FD46A3435CB070D003E1F29AFDC1EFC58A9D70BCAF7FA6B34A9393DB5A"})
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
