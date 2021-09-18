from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from shit_dict import *
from shit_methods import *

PATH = '/Users/assanbekkaliyev/Downloads/chromedriver'
driver = webdriver.Chrome(PATH)
driver.get('http://register.ndda.kz/register.php/mainpage/reestr/lang/ru')

try: 
    search_handler(driver)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ui-row-ltr')))
except Exception as e: 
    print(e)

parent_rows = driver.find_elements_by_class_name('ui-row-ltr')

data = []

for index, row in enumerate(parent_rows):
    cells = parent_rows[index].find_elements_by_tag_name('td')
    del cells[15:21]
    general_info = { general_info_keys[i]: cells[i].text for i in range(len(general_info_keys)) }

    # new item open
    info_link = row.find_element_by_class_name('openReestr')
    info_link.click()
    time.sleep(3)

    # go through tabs
    next_tab(driver, 0)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[0]}"]//tbody//tr')[1:]
    order_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        order_info_row = { order_keys[i]: cells[i].text for i in range(len(order_keys)) }
        order_info.append(order_info_row)
    
    # go through tabs
    next_tab(driver, 1)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[1]}"]//tbody//tr')[1:]
    manufacturer_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        manufacturer_info_row = { manufacturer_keys[i]: cells[i].text for i in range(len(manufacturer_keys)) }
        manufacturer_info.append(manufacturer_info_row)

    # go through tabs
    next_tab(driver, 2)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[2]}"]//div[@id="yw1"]//tbody//tr')
    package_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        package_info_row = { package_keys[i]: cells[i].text for i in range(len(package_keys)) }
        package_info.append(package_info_row)

    next_tab(driver, 3)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[3]}"]//tbody//tr')
    instructions_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        instructions_info_row = { instructions_keys[i]: cells[i].text if len(get_child(cells[i])) == 0 else get_child(cells[i])[0].get_attribute('href') for i in range(len(instructions_keys)) }
        instructions_info.append(instructions_info_row)

    # go through tabs
    next_tab(driver, 4)

    rows = driver.find_elements_by_xpath(f'//div[@id="{tab_list[4]}"]//tbody//tr')[1:]
    certificate_info = []

    for index, row in enumerate(rows):
        cells = rows[index].find_elements_by_tag_name('td')
        certificate_info_row = { certificate_keys[i]: cells[i].text for i in range(len(certificate_keys)) }
        certificate_info.append(certificate_info_row)

    # merge all subdata
    item = { 
        'general_info': general_info, 
        'order_info': order_info, 
        'manufacturer_info': manufacturer_info, 
        'package_info': package_info, 
        'instructions_info': instructions_info, 
        'certificate_info': certificate_info 
        }

    # find close button and close current window
    driver.find_element_by_class_name('close').click()

# insert product item data into global data list
data.append(item)