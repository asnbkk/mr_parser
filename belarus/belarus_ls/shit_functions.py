import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from shit_chrome_path import *
# from shit_dict import tab_list
from kafka import KafkaProducer

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.ID, 'FProps_0__CritElems_0__Val')))
        search_input.send_keys(' ')
        search_input.submit()
    except Exception as e: 
        print(e)  