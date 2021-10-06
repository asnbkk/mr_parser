import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['185.146.3.170:9092'],
    api_version=(0,11,5),
    value_serializer=lambda x: 
    json.dumps(x).encode('utf-8')
    )

def send_data(data):
    producer.send('testTopic', value=data)

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'id_q_mi_label_application')))
        search_input.send_keys('а')
        search_input.submit()
    except Exception as e: 
        print(e)   

def wait_table(driver):
    try:
        return WebDriverWait(driver, 600).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'data-fancybox')))
    except:
        print('smth is wrong')
        pass

def text_prep(text):
    return text.replace('"', '').replace('\n', ' ')