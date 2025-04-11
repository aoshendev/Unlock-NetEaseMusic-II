# coding: utf-8

import os
import time
import logging
import zipfile
import urllib.request
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# === 配置 ===
CHROME_DIR = "chrome-win64"
CHROMEDRIVER_DIR = "chromedriver-win64"
COOKIE_MUSIC_U = "0092F055425C76D0DBC620FFBF7E31493E58FEE462574A576BEDC54FD7DE6D1EECFDB0FD3BA7C52891E66FB220FF75D0C74BA5900A2862320E16AC173DBDD833C815E291C6804E55E8B419512744687C72A191A19B3E756C6B59BBB08B5DC0C686EF370157E81862D65F1B350AAE010D00B0F4706EA85C9D98D5263EDC3BB4AC208C0B87E7C606834AA70DFCE4B0DC28DB3DC44C5E66CB346ED60296461C07DB8EFB605D1FD09F31DDF6FC409EB4AC70856F07F0CB1BA05D33EA1449417311CFDF9C16F03D6B4B3CDB347B880DAF6795B150F46E9E524CC432486ED8C14F5D886FF09ED4E05338C4AE952C07D3BCA7CB5A8F51368C136DF1D28DE4FB63811B0BA2CC6A7D2D7321100056D652ACE07417B1DECCA487607DB132F327CF12F83953192C7B9032ABB01AC22489BECA2C2215ADEFD8E9FAC5E00648A8123929C80FBF8EB7A82919D1ABC7979EA72B28A5E7865B36E5B3196DCCD968565E3A3DDD4346EE"  # ← 请替换为你的真实 Cookie

# === 日志配置 ===
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

def download_and_extract(url, output_dir):
    zip_path = output_dir + ".zip"
    logging.info(f"⬇️ Downloading: {url}")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    os.remove(zip_path)

def prepare_chrome_and_driver():
    logging.info("🔍 Fetching latest Chrome version info from Google")
    meta_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    with urllib.request.urlopen(meta_url) as response:
        data = json.loads(response.read())

    version = data["channels"]["Stable"]["version"]
    logging.info(f"✅ Latest Stable Chrome: {version}")

    chrome_url = data["channels"]["Stable"]["downloads"]["chrome"][3]["url"]  # win64
    driver_url = data["channels"]["Stable"]["downloads"]["chromedriver"][3]["url"]  # win64

    if not os.path.exists(CHROME_DIR):
        download_and_extract(chrome_url, CHROME_DIR)
    if not os.path.exists(CHROMEDRIVER_DIR):
        download_and_extract(driver_url, CHROMEDRIVER_DIR)

    return (
        os.path.abspath(f"{CHROME_DIR}/chrome.exe"),
        os.path.abspath(f"{CHROMEDRIVER_DIR}/chromedriver.exe")
    )

def run_unlock(chrome_path, chromedriver_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension("NetEaseMusicWorldPlus.crx")
    chrome_options.binary_location = chrome_path

    service = Service(chromedriver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(20)

    browser.get("https://music.163.com")
    logging.info("🍪 Injecting MUSIC_U Cookie")
    browser.add_cookie({
        "name": "MUSIC_U",
        "value": COOKIE_MUSIC_U,
        "domain": ".music.163.com"
    })

    browser.refresh()
    time.sleep(5)
    browser.save_screenshot("debug_after_cookie.png")
    logging.info("📸 Screenshot saved as debug_after_cookie.png")

    logging.info("✅ Cookie login done. Waiting before quit...")
    time.sleep(10)
    browser.quit()

if __name__ == "__main__":
    try:
        chrome_path, chromedriver_path = prepare_chrome_and_driver()
        run_unlock(chrome_path, chromedriver_path)
    except Exception as e:
        logging.error(f"❌ Failed: {e}")
