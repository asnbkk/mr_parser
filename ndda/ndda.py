from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from shit_dict import *

PATH = '/Users/assanbekkaliyev/Downloads/chromedriver'
driver = webdriver.Chrome(PATH)
# ебать мой хуй, это оказывается iframe. У него другая ссылка
driver.get('http://register.ndda.kz/register.php/mainpage/reestr/lang/ru')

def search_handler():
    try: 
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ReestrTableForNdda_name')))
        search_input.submit()
    except Exception as e: 
        print(e)   

try: 
    search_handler()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ui-row-ltr')))
    # сука нахуй такие конченные сайты делать блять
except Exception as e: 
    print(e)

rows = driver.find_elements_by_class_name('ui-row-ltr')

for index, row in enumerate(rows):
    cells = rows[index].find_elements_by_tag_name('td')
    del cells[15:21]
    general_info = { general_info_keys[i]: cells[i].text for i in range(len(general_info_keys)) }

    # открыть новую вкладку
    info_link = row.find_element_by_class_name('openReestr')
    info_link.click()
    time.sleep(3)

    tab = driver.find_element_by_xpath(f'//a[@href="#{tab_list[0]}"]')
    tab.click()
    time.sleep(3)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[0]}"]//tbody//tr')[1:]
    order_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        order_info_row = { order_keys[i]: cells[i].text for i in range(len(order_keys)) }
        order_info.append(order_info_row)
    
    # print(general_info_row)
    # print('---')