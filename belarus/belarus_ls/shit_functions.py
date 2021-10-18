import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from shit_chrome_path import *
# from shit_dict import tab_list

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=[kafka_host],
    api_version=(0,10,1),
    value_serializer=lambda x: 
    json.dumps(x).encode('utf-8')
    )

def send_data(data):
    producer.send('testTopic', value=data)

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.ID, 'FProps_0__CritElems_0__Val')))
        search_input.send_keys(' ')
        search_input.submit()
    except Exception as e: 
        print(e)  

def open_prod(cell, driver):
    actionChains = ActionChains(driver)
    actionChains.click(cell).perform()

def pagination(current_page, driver):
    tab = driver.find_element_by_xpath(f'//div[@class="page-view"]//ul//li/following-sibling::li[1]//a[text()[contains(.,"{current_page + 1}")]]')
    open_prod(tab, driver)
    # print(len(tabs))