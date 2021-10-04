import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
        return WebDriverWait(driver, 300).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'data-fancybox')))
    except:
        print('smth is wrong')
        pass

# def next_page_handler(driver):
    # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'DataTables_Table_1_next'))).click()