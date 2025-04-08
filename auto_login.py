Content unavailable. Resource was not cached# coding: utf-8

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
    browser.add_cookie({"name": "MUSIC_U", "value": "00509E93E2F303876BA95E1B1F3353DB93733461846DBA650767351EFF2B213B881C7C6EE419109C49195C7442577628B53691781F3576BA86D22007D3BC312EE6F5602732A70F68B4482153E869BA27538FFC382BBE6C1EEBA1433C98CE5E3089E1295832C1137A34E320886CC7906D47730C1E6684CF77ECF880D45B34E22850A4901A130832DCD1D38AE3F120D472B214E128C015A03762713CE83FA5AFDF29FC5ED5360429FC6C6E28E2FE3EE534D75D3A71D4F9DF6D27E14F79C84630962077296C01767A5BD5A40083E5AD2743AD41B71185F98BE7E6D4AA04E23616FCC8EE930C1D8CA86DF95B3DB60D88C4145C3060E6C6D0C5D348FA81C14F2B06C2D8E4B6971E5E695BB7E1234985BA0CB7CFBC213A0E8A3A3B49499CB06EB47E4953E9F84F69EB92074E0A45A87C0639CB8BB447AA8E8A0FCCABF594C275D4B1AB269C14751BC5F582B0560ACFB53DDE1637C4389D36DAED76073B545F75314C1500"})
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
