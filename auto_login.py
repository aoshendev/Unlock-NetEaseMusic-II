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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F8BAAA0DE2D17FE6344EB7EFEE63E02AA2FA53D4B54D99F14C48ED7F6FFB5D734FFA426B9B0E58E88D7475F9103D100A02518C383B601366D94C09B4B0809829E1FF0F4DF57835F64AAB553AF08D8AFC20F5CC8093C8B60C10F9EBD5C31A6E60A89E74E532B709378265784F12D7EF90F6056127644A304ADB480988CAB8E1B7F4C476D3482761F2D30B422CC0EEC5227BAA6C119B9CB11921FC3C566D650F706B4189C5F1DBD39B65A91D3173B1FE73BA9EDED92B1549AA9BC351E816C4FD3D73A9F9255A08454DA33AEB2794D9A31D924E28613F57C09FA87D9B346C486450757F97C2D836D53F9B716D3145EC8F4248E0D37C65A839C0756A6262B516D4491BBF04F9AAA261F01F138889850C4486D98F3378F6F16E42F893F304F29E89AA33D46418FE98BFA069AB6ED24B32A4581519641D43E6FB7DEFE24142AD45B943ABA39859BECA0C7C186FBCE27F8A9E18C32D55A47803E99589910948FD550DC1"})
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
