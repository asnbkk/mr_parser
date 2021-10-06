from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def wait_for_table(driver):
    try:
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.ID, 'row_0.0')))
    except:
        print('this page sucks')

def new_driver(driver, current_page=None):
    try: 
        wait_for_table(driver)
    except: 
        print('ah shit page again')
        driver.refresh()
        wait_for_table(driver)
        set_page_number(driver, current_page)
        time.sleep(10)

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