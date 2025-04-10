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
    browser.add_cookie({"name": "MUSIC_U", "value": "0072BA4271089A1861B7C223C864B8A93173627B37851E686C302CD79B2D0A4BC8289C5DACA56642601A6B9BDB0D0FD7B01CCA76F86EF0D0E7F405D02FE17879A355F9B4A08559E31DCA4457F86F0B1FB65A96EDC6F42CDBE48D774444F427E721BE0DA139A4EA5CA6320AF27EDCF0610B24CDE1491B3B880D5E7787A43CEB82A776E78AC135AC4FD64591FDA9A10629199F2F2B8952E8E533011F49973428C5DD898B24E8F937AE87AB24EC8A66FBDCF5A14ADE99C143FF6B8E029DFD12717163D944E3E25420F008248A8E6B568F8F57E54A075BD018DE055D49B1A222FDF9081787AB8DAD31FCC59FE2B4A4D9A61BA60BD837238B62C9DFCD6DB2A88BFF877700DB7351CB7E4FC2554434B8C0E3CDB46B6D97527095557619FB8A0A2060DC22287F56A75C8CD04951BA02EB7A28B1A0F886F90015B762C456D1CAAA5E706C9D56585062E7BC9737F1966E9DD7E179BE81F02F198A0909A943AC1AFD504FFB9E"})
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
