import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from shit_chrome_path import *
from shit_dict import tab_list
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=[kafka_host],
    api_version=(0,10,1),
    value_serializer=lambda x: 
    json.dumps(x).encode('utf-8')
    )

def send_data(data):
    producer.send('testTopic', value=data)

def get_child(element):
    return element.find_elements_by_xpath(".//*")

def next_tab(driver, index):
    try:
        tab = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'//a[@href="#{tab_list[index]}"]')))
        ActionChains(driver).move_to_element(tab).click(tab).perform()
    except:
        print('Currently the site suck. Please cum later')

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ReestrTableForNdda_name')))

        # select = Select(driver.find_element_by_id('ReestrTableForNdda_reg_type'))
        # select.select_by_visible_text('МИ')

        search_input.submit()
    except Exception as e: 
        print(e)   

def table_check(driver, class_name):
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except Exception as e: 
        print(e)

def wait_table(driver, index, delete_first, is_nested=False):
    add_element = '//div[@id="yw1"]' if is_nested else ''
    try:
        element = WebDriverWait(driver, 300).until(
            EC.visibility_of_all_elements_located((By.XPATH, f'//div[@id="{tab_list[index]}"]{add_element}//tbody//tr')))
        return element[1:] if delete_first else element
    except:
        pass

def text_prep(text):
    return text.replace('"', '').replace('\n', ' ')