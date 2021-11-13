import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
from shit_chrome_path import *

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=[kafka_host],
    api_version=(0,10,1),
    value_serializer=lambda x: 
    json.dumps(x).encode('utf-8')
    )

def send_data(data):
    producer.send('testTopic', value=data)

def search_handler(driver, year):
    try: 
        toggle = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'js-open-extended-form')))
        toggle.click()
        # time.sleep(5)
        start_date = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, 'id_dt_ru-start')))
        start_date.click()
        start_date.send_keys(f'0101{year - 1}')
        time.sleep(2)
    
        end_date = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, 'id_dt_ru-end')))
        end_date.click()
        end_date.send_keys(f'0101{year}')

        time.sleep(1)
        end_date.submit()

        # search_input = WebDriverWait(driver, 300).until(
        #     EC.presence_of_element_located((By.ID, 'id_q_mi_label_application')))
        # search_input.send_keys('фор')
        # search_input.submit()
    except Exception as e: 
        print('hello')
        print(e)   

def wait_table(driver):
    return WebDriverWait(driver, 300).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'data-fancybox')))

def text_prep(text):
    temp_text = text.get_attribute('title') if text.get_attribute('title') else text.text
    return temp_text.replace('"', '').replace('\n', ' ')