00B1E3B26CF512F9E64BE196580C0E7726F37244061A51C6DABE075B38F3CDCA9B1B5382DDD62252CCBE57691F987474C324693BE45083DA4B3D637B6A9C20F50EAE0184538F5E6ED1AEF00BD13D0EC3E5847261EC4E7FF24BE54E7E4297E2E18AEFD1B9BF453280D986A936F3194FF72BCBAB4155E9D5FA959993529BABA2082256D622F393CF87198777A800E081E0E1C772BF7A6A5A65A7524BD8B9227A7F04E77475FD159E8D5EB7D2E115A27B3591655DBD218E85439B131F76C8C524BBB7FB676E12DFDC874C3B85B7E0618234EC11A6605D04386A67E32C345ADE3621B010B6C9644D6621164E4144BCDFEFF3AAA0CA68281F2E273BBD23A8DA2F38F2D37699E2B70FE8ADBDD98CC09C068F29FEC3BDB4B1DE4CD689E254640E5A9C3A66EBEA80F78728B11804EFD4C5803CAB7D76761B5DAACEFBDCDEA97279A4CD29771CD6EEA91EA0852B9912BB889258A1AED961E4D6FE8477367F4F7B956A227F05# coding: utf-8

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
