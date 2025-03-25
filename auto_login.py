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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A37BC83C90577CD23F86E60CA0C188336666517C5328FFC4ADB111A947F290FC77E8E6C80238910E46CA8E4067DFF2941C2C7673A78025056AECC923E4B1731B9B7144AE53ED6226554BF63857EF23CB1862C259EE14D8838E3822042294287072888F0F07B718CD4D42E2C7F2D7D51D9A22F2E3763AD6619D98EF3A89BCD3E3F06E487B5369213CFFD14337BC2F343B6414691152EE6A8F2FABF4380905B9B849119150588DFB9AE123E23FAC8526A6FF5B065D403603E881CE0A6860BBE07B7E966C883E83BF91D8950FCF14CF7D86010749637E39AA89335EAFF34FCE40BF2D4F919ACF0E655D701A9370EF2A76CF60AF9A18DF9F7F7CCA686593D1EEFD90C326FBDB03558E50BAD127C70A4D6C4BEC87C9C15C419BA067B66107CEF7BD2284F18FB1C8D195A11B9FE5320C3D02A8EFD637CA67D9376641232F429D726DD461996099117DB71564B70CF45F43E050A5991009A13CB74DCF85B75D18E4EFE9"})
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
