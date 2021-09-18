from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from shit_dict import tab_list

def get_child(element):
    return element.find_elements_by_xpath(".//*")

def next_tab(driver, index):
    tab = driver.find_element_by_xpath(f'//a[@href="#{tab_list[index]}"]')
    table_check(driver, 'active')
    ActionChains(driver).move_to_element(tab).click(tab).perform()

def search_handler(driver):
    try: 
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ReestrTableForNdda_name')))
        search_input.submit()
    except Exception as e: 
        print(e)   

def table_check(driver, class_name):
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except Exception as e: 
        print(e)