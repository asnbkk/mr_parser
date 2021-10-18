from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from shit_functions import *

def process_parser():
    return 0

def bootstrap():
    while True:
        # print('timer for 3 secs')
        # time.sleep(3)
        opts = webdriver.ChromeOptions()
        # opts.add_argument("--headless")
        # opts.add_argument("--disable-xss-auditor")
        # opts.add_argument("--disable-web-security")
        # opts.add_argument("--allow-running-insecure-content")
        # opts.add_argument("--no-sandbox")
        # opts.add_argument("--disable-setuid-sandbox")
        # opts.add_argument("--disable-webgl")
        # opts.add_argument("--disable-popup-blocking")

        PATH = chrome_path
        driver = webdriver.Chrome(PATH, options=opts)
        url = 'https://www.rceth.by/Refbank/reestr_lekarstvennih_sredstv/results'
        driver.get(url)

        search_handler(driver)
        time.sleep(10)

bootstrap()