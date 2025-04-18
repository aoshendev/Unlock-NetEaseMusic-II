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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DB6D13D8C57F821212D2681E40CDFEC880D0002B4208B1A519A9D966787A7EC923A17B7D812C5DF6080C94DDF0814E8151822B6A144682F2E0063ABA60234CA9BDB98C42F57944ADD7E143D3281F0B2C59A11D8ED83D9127D30AE717AF82D8C32CF5508D16A2525855377713F47E630135D7430126D7EF5D9FBFE56ED1999B430D3A51FC88C85C5F740C278563915C679B6527379DED27C89D1FD6A0DD3D2187A1C8031E8FF0318873B917C9AD12D1B1C3398949A914D99C22E63C2399275DD8EC0048EF98C36B8E1F8AD774E91EE2F4882585A7C3C3416D9C7A6E30BDC81F49A3F4AD49F4CAA4B70E23E5446FC85429EBB8B6ED702C34F08E0774F892F6DF83E61BE74E6D89B9C498E23988A097E7AC5911858641FB9BC5BE0907D14218DE94BCD4B132AB8515FAE0E890B47BC97E897DC05E7639ECC2FB5ED83825D4914914"})
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
