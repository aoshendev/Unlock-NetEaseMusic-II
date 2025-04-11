# coding: utf-8

import os
import time
import logging
import zipfile
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retrying import retry

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

CHROME_DIR = "chrome-win64"
CHROMEDRIVER_DIR = "chromedriver-win64"

CHROME_URL = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/win64/chrome-win64.zip"
CHROMEDRIVER_URL = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/win64/chromedriver-win64.zip"

def download_and_extract(url, output_dir):
    zip_path = output_dir + ".zip"
    if not os.path.exists(output_dir):
        logging.info("\u2b07\ufe0f Downloading: {}".format(url))
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        os.remove(zip_path)

def prepare_browser():
    download_and_extract(CHROME_URL, CHROME_DIR)
    download_and_extract(CHROMEDRIVER_URL, CHROMEDRIVER_DIR)

    chrome_path = os.path.abspath(os.path.join(CHROME_DIR, "chrome.exe"))
    chromedriver_path = os.path.abspath(os.path.join(CHROMEDRIVER_DIR, "chromedriver.exe"))

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_path
    chrome_options.add_extension("NetEaseMusicWorldPlus.crx")

    service = Service(chromedriver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(20)
    return browser

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]"))
        )
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error("Failed to enter iframe: {}".format(e))
        browser.save_screenshot("debug_iframe.png")
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    logging.info("Initializing Chrome WebDriver (fixed version 134.0.6998.88)")

    try:
        browser = prepare_browser()
    except Exception as e:
        logging.error("❌ Failed to initialize ChromeDriver: {}".format(e))
        return

    browser.get("https://music.163.com")

    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({
        "name": "MUSIC_U",
        "value": "你的COOKIE在这里替换",
        "domain": ".music.163.com"
    })

    browser.refresh()
    time.sleep(5)
    browser.save_screenshot("debug_after_cookie.png")
    logging.info("✅ Cookie login successful")

    logging.info("Unlock finished")
    time.sleep(10)
    browser.quit()

if __name__ == "__main__":
    try:
        extension_login()
    except Exception as e:
        logging.error("❌ Failed to execute login script: {}".format(e))
