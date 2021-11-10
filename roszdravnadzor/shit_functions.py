import time
from selenium.webdriver.common.by import By
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

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.ID, 'id_q_mi_label_application')))
        search_input.send_keys('а')
        search_input.submit()
    except Exception as e: 
        print(e)   

def wait_table(driver):
    return WebDriverWait(driver, 300).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'data-fancybox')))

def text_prep(text):
    temp_text = text.get_attribute('title') if text.get_attribute('title') else text.text
    return temp_text.replace('"', '').replace('\n', ' ')