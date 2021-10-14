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

# page_amount = int(driver.find_element_by_id('sp_1_register_pager').text)
# for page in range(page_amount):
while True:
    parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
    prev_rows = parent_rows
    
    for index, row in enumerate(parent_rows):
        cells = parent_rows[index].find_elements_by_tag_name('td')
        general_info = cells[1:7]
        shelf_life = cells[14]

        # 15 20
        attributes = cells[15:21]
        attributes_list = []
        
        for index, attr in enumerate(attributes):
            if attr.find_element_by_tag_name('input').get_attribute('checked') == 'true':
                attributes_list.append(attributes_keys[index])
        
        general_info = { general_info_keys[i]: text_prep(general_info[i].text) for i in range(len(general_info_keys)) }
        
        main_info = { 
            **general_info, 
            'shelfLife': text_prep(shelf_life.text), 
            'appointment': '', 
            'fieldOfUse': '', 
            'securityClass': '',
            'shortTechDescription': '',
            'attributes': ','.join(attributes_list),
            'shelfLifeComment': ''}

        # new item open
        WebDriverWait(row, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'openReestr'))).click()
        table_check(driver, 'modal-open')

        next_tab(driver, 0)
        rows = wait_table(driver, 0, True)
        order_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            order_info_row = { order_keys[i]: text_prep(cells[i].text) for i in range(len(order_keys)) }
            order_info.append(order_info_row)
        
        next_tab(driver, 1)
        rows = wait_table(driver, 1, True)
        manufacturer_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            manufacturer_info_row = { manufacturer_keys[i]: text_prep(cells[i].text) for i in range(len(manufacturer_keys)) }
            manufacturer_info.append(manufacturer_info_row)

        next_tab(driver, 2)
        rows = wait_table(driver, 2, False, True)
        package_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            name = text_prep(cells[0].text)

            if cells[1].find_element_by_tag_name('input').get_attribute('checked') == 'true':
                is_primary = True
            else: 
                is_primary = False
            
            cells_rest = cells[2:]
            package_info_row = { package_keys[i]: text_prep(cells_rest[i].text) for i in range(len(package_keys)) }

            package_info_row_data = {
                'name': name,
                'primary': is_primary,
                **package_info_row
            }

            package_info.append(package_info_row_data)

        next_tab(driver, 3)
        rows = wait_table(driver, 3, False)
        instructions_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            instructions_info_row = { instructions_keys[i]: text_prep(cells[i].text) if len(get_child(cells[i])) == 0 else get_child(cells[i])[0].get_attribute('href') for i in range(len(instructions_keys)) }
            instructions_info.append(instructions_info_row)

        next_tab(driver, 4)
        rows = wait_table(driver, 4, True)
        certificate_info = []

        for index, row in enumerate(rows):
            cells = rows[index].find_elements_by_tag_name('td')
            certificate_info_row = { certificate_keys[i]: text_prep(cells[i].text) for i in range(len(certificate_keys)) }
            certificate_info.append(certificate_info_row)

        website = {
            'name': 'ndda.kz',
            'country': ''
        }

        # merge all subdata
        item = { 
                'mainInfo': main_info, 
                'decrees': order_info, 
                'manufacturers': manufacturer_info, 
                'completeness': [],
                'variants': [],
                'instructions': instructions_info, 
                'certificates': certificate_info,
                'packages': package_info, 
                'nmirks': [],
                'website': website
            }

        print(item['mainInfo']['productName'])
        print('-')
        
        # sending data by kafka
        send_data(item)
        
        # find close button and close current window
        driver.find_element_by_class_name('close').click()

        # insert product item data into global data list and write to the file
        data.append(item)
        with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print(len(data))
    
    # go to the next page if possible; else break the loop
    try:
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'next_register_pager'))).click()
    except:
        print('seems to be the end')
        break

    # shit time sleep
    try: 
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'load_register_grid')))
        parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
    except:
        print('ah shit')
        time.sleep(10)