from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
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

def wait_for_table(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'row_0.0')))

def new_driver(driver, current_page=None):
    try: 
        wait_for_table(driver)
    except: 
        print('ah shit page again')
        driver.refresh()
        wait_for_table(driver)
        set_page_number(driver, current_page)
        time.sleep(10)

def get_general_information_by_id(driver):
    panel2_list = driver.find_elements_by_xpath("//div[@id='panel2']//ul//li")
    panel2_keys = []
    for row in panel2_list:
        panel2_keys.append(row.get_attribute('id'))
    panel2 = { panel2_keys[i]: panel2_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(panel2_keys)) }
    return panel2

def double_click(row, driver):
    actionChains = ActionChains(driver)
    actionChains.double_click(row).perform()

def tab_click(tabs, index):
    tabs[index].click()
    time.sleep(2)

def merge_general_info(header, mnn, release_form_list, manufacturer, char_of_med_product):
    return {
        'header': header,
        'mnn': mnn,
        'release_form_list': release_form_list,
        'manufacturer': manufacturer,
        'char_of_med_product': char_of_med_product
        }

def merge_position(general_info, panel1, reg_data, panel2, panel4, manufacturings_list, regulations, substances):
    return {
        'general_info': general_info, 
        'panel1': panel1,
        'reg_data': reg_data,
        'panel2': panel2,
        'panel4': panel4,
        'manufacturings_list': manufacturings_list,
        'regulations': regulations,
        'substances': substances
        }

def text_prep(text):
    return text.replace('"', '').replace('\n', ' ')

def get_current_page_number(driver):
    return driver.find_element_by_class_name('ecc-page-number-input').get_attribute('placeholder')

def set_page_number(driver, current_page):
    try: 
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ecc-page-number-input')))
        search_input.send_keys(str(int(current_page) + 2))
        # search_input.submit()
        new_driver(driver)
    except Exception as e: 
        print(e)