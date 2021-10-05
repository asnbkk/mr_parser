from shit_dict import *
from shit_functions import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

PATH = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH)
driver.get('https://portal.eaeunion.org/sites/commonprocesses/ru-ru/Pages/DrugRegistrationDetails.aspx')

data = []
new_driver(driver)

while True:
    table = driver.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_tag_name('tr')

    for index, row in enumerate(rows):
        cells = row.find_elements_by_tag_name('td')
        header = text_prep(cells[0].text)
        mnn = cells[1].text
        manufacturer = cells[3].text

        release_form_list = []
        for item in cells[2].find_elements_by_tag_name('li'):
            release_form_list.append(text_prep(item.text))

        char_of_med_product = []
        for item in cells[4].find_elements_by_tag_name('li'):
            char_of_med_product.append(text_prep(item.text))

        general_info = merge_general_info(header, mnn, release_form_list, manufacturer, char_of_med_product)

        # double click does not work 
        while len(driver.window_handles) < 2:
            double_click(row, driver)

        # details
        driver.switch_to.window(driver.window_handles[1])
        try: 
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'bordered-list__item-content')))

            # data from panel1 list
            panel1_list = driver.find_elements_by_xpath("//div[@id='panel1']//ul//li")
            panel1 = { panel1_keys[i]: text_prep(panel1_list[i].find_element_by_class_name('zebra-list__content').text) for i in range(len(panel1_keys)) }

            # registration full data
            reg_data_list = driver.find_elements_by_xpath("//div[@id='registrations-list']//div[@class='zebra-list']//ul//li")

            toggle_button = driver.find_element_by_class_name('product-list__trigger-icon').click()
            time.sleep(2)
            
            reg_data = { reg_data_keys[i]: text_prep(reg_data_list[i].find_element_by_class_name('zebra-list__content').text) for i in range(len(reg_data_keys)) }

            # list of left tabs
            tabs = driver.find_elements_by_xpath("//div[@class='left-menu__list']//ul//li")

            # get data from panel 2
            tab_click(tabs, 1)

            # md is medicinal product
            panel2 = get_general_information_by_id(driver)

            # get data from panel 4
            panel4 = []
            panel4_table_rows = driver.find_elements_by_xpath("//div[@id='panel4']//tbody//tr")[1:]

            for panel4_table_row in panel4_table_rows:
                table_cell = panel4_table_row.find_elements_by_class_name('table__cell')[1:]
                panel4_row = { panel4_keys[i]: text_prep(table_cell[i].text) for i in range(len(panel4_keys)) }
                panel4.append(panel4_row)

            # manufacturings-list toggle button
            tab_click(tabs, 2)

            manufacturings_list = []
            product_list = driver.find_elements_by_xpath("//div[@id='manufacturings-list']//ul//li[@class='product-list__item']")

            for index, product_item in enumerate(product_list):
                # open new tab
                product_list[index].find_element_by_class_name('product-list__trigger-icon').click()
                time.sleep(1)

                product_manufacturings_list = product_list[index].find_elements_by_class_name('zebra-list__item')
                manufacturings_row = { product_manufacturings_keys[i]: text_prep(product_manufacturings_list[i].find_element_by_class_name('zebra-list__content').text) for i in range(len(product_manufacturings_keys)) }

                # production sites
                # trying to figure out is there production_sites_list table
                try:
                    production_sites_list = product_list[index].find_elements_by_class_name('table__cell')[4:]
                    production_sites_row = { production_sites_keys[i]: text_prep(production_sites_list[i].text) for i in range(len(production_sites_keys)) }
                except:
                    production_sites_row = { production_sites_keys[i]: '' for i in range(len(production_sites_keys)) }

                # merging tow intermediate dicts and appending to list
                manufacturings_list.append({**manufacturings_row, **production_sites_row})

            # regulations toggle button
            tab_click(tabs, 3)

            regulations = []
            regulations_table_rows = driver.find_elements_by_xpath("//div[@id='panel5']//tbody//tr")[1:]

            for regulations_table_row in regulations_table_rows:
                table_cell = regulations_table_row.find_elements_by_class_name('table__cell')

                regulations_row_text = { regulations_keys[i]: text_prep(table_cell[i].text) for i in range(len(regulations_keys)) }
                document_link = { 'document_link': regulations_table_row.find_element_by_class_name('link').get_attribute('href') }
                # merging tow intermediate dicts and appending to list
                regulations_row = {**regulations_row_text, **document_link}
                regulations.append(regulations_row)

            # pharmaceutical substances toggle button
            tab_click(tabs, 4)

            substances = []
            substances_table_rows = driver.find_elements_by_xpath("//div[@id='panel6']//tbody//tr")[1:]

            for substances_table_row in substances_table_rows:
                table_cell = substances_table_row.find_elements_by_class_name('table__cell')

                substances_row_text = { substances_keys[i]: text_prep(table_cell[i].text) for i in range(len(substances_keys)) }
                # merging tow intermediate dicts and appending to list
                substances.append(substances_row_text)

        except Exception as e: 
            # handle shit
            print(e)
            print(f'some problems with {header}')
        finally: 
            # merge all data inside one position and append to data list
            position = merge_position(general_info, panel1, reg_data, panel2, panel4, manufacturings_list, regulations, substances)

            data.append(position)
            print(len(data))
            print(position['general_info']['header'])

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    try:
        next_page_button = driver.find_element_by_class_name('arrow-right').click()
        time.sleep(5)
        new_driver(driver)
        
    except: 
        print('this is the end!')
        break

driver.quit()