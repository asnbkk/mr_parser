from selenium import webdriver
from shit_dict import *
from shit_methods import *
import time
import json

PATH = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH)
driver.get('http://register.ndda.kz/category/search_prep')

frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "iframe1")))
driver.switch_to.frame(frame)

search_handler(driver)
table_check(driver, 'ui-row-ltr')

data = []

page_amount = int(driver.find_element_by_id('sp_1_register_pager').text)
for page in range(page_amount):

    parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
    prev_rows = parent_rows
    
    for index, row in enumerate(parent_rows):
        cells = parent_rows[index].find_elements_by_tag_name('td')

        del cells[15:21]
        general_info = { general_info_keys[i]: cells[i].text for i in range(len(general_info_keys)) }

        # new item open
        WebDriverWait(row, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'openReestr'))).click()
        table_check(driver, 'modal-open')

        next_tab(driver, 0)
        rows = wait_table(driver, 0, True)
        order_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            order_info_row = { order_keys[i]: cells[i].text for i in range(len(order_keys)) }
            order_info.append(order_info_row)
        
        next_tab(driver, 1)
        rows = wait_table(driver, 1, True)
        manufacturer_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            manufacturer_info_row = { manufacturer_keys[i]: cells[i].text for i in range(len(manufacturer_keys)) }
            manufacturer_info.append(manufacturer_info_row)

        next_tab(driver, 2)
        rows = wait_table(driver, 2, False, True)
        package_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            package_info_row = { package_keys[i]: cells[i].text for i in range(len(package_keys)) }
            package_info.append(package_info_row)

        next_tab(driver, 3)
        rows = wait_table(driver, 3, False)
        instructions_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            instructions_info_row = { instructions_keys[i]: cells[i].text if len(get_child(cells[i])) == 0 else get_child(cells[i])[0].get_attribute('href') for i in range(len(instructions_keys)) }
            instructions_info.append(instructions_info_row)

        next_tab(driver, 4)
        rows = wait_table(driver, 4, True)
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

        print(item['general_info']['reg_number'])
        print('-')
        
        # find close button and close current window
        driver.find_element_by_class_name('close').click()

        # insert product item data into global data list
        data.append(item)
        print(len(data))
    
    # go to the next page
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'next_register_pager'))).click()
    # shit time speep
    try: 
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'load_register_grid')))
        parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
    except:
        print('ah shit')
        time.sleep(10)