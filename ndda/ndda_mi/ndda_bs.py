from selenium import webdriver
from shit_dict import *
from shit_methods import *
from shit_chrome_path import *
# from json2html import *
import time

import random
# import json

from bs4 import BeautifulSoup
import requests

def get_data(id):
    r = requests.get(f'http://register.ndda.kz/register.php/mainpage/viewReestrData/{id}')
    return BeautifulSoup(r.json()['body'], 'lxml')

state = 'parsing'
data = []
data_counter = 0

def process_parser(driver):
    while True:
        try:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            current_page = driver.find_element_by_xpath('//td[@id="input_register_pager"]//input').get_attribute("value")
        except:
            global state
            state = 'not available'
            print('shit here')

        global data_counter
        for i, row in enumerate(soup.find_all('tr', {'class': 'ui-row-ltr'})):
            try:
                p_cells = row.find_all('td')
                attributes = p_cells[15:21]
                
                reg_number = p_cells[0]
                attributes_list = []
                print(f'STARTING:\n{p_cells[2].text}')

                row_id = row.find('td').find('a').get('data-rowid')
                soup = get_data(row_id)


                main_table = soup.find('div', {'id': 'yw4_tab_1'}).find('form').find('table').find_all('td')[1::2]

                # kill this shit
                for index, attr in enumerate(attributes):
                    if attr.find('input').has_attr('checked'):
                        attributes_list.append(attributes_keys[index])

                # attributes = soup.find_all('label', {'class': 'checkbox'})
                # for index, attr in enumerate(attributes):
                #     if attr.select('label > input')[1].has_attr('checked'):
                #         attributes_list.append(attributes_keys[index])

                try:
                    general_info_rows = main_table[:11]
                    attributes = p_cells[15:21]
                    
                    general_info = {general_info_keys[i]: text_prep(general_info_rows[i].text) for i in range(len(general_info_keys))}
                    main_info = {
                        **general_info, 
                        'reg_number': text_prep(reg_number.text),
                        'shelfLifeComment': text_prep(main_table[-2].text), 
                        'attributes': ','.join(attributes_list),
                        'dosage': '',
                        'lsType': ''}
                    print('main info: ok')
                except Exception as e:
                    print(e)
                    print('main_info: - ')

                try:
                    secondary_table = soup.find('table', {'class', 'table table-bordered table-hover'})
                    secondary_table_rows = secondary_table.find_all('tr')[1:]
                    nmirks = []
                    for row in secondary_table_rows:
                        cells = row.find_all('td')
                        nmirk = {nmirk_keys[i]: text_prep(cells[i].text) for i in range(len(nmirk_keys))}
                        nmirks.append(nmirk)
                    print('nmirks: ok')
                except:
                    print('nmirks: -')
                    
                try:
                    rows = soup.find('div', {'id': 'yw4_tab_2'}).find('table').find_all('tr')[1:]
                    order_info = []
                    for row in rows:
                        cells = row.find_all('td')
                        order_info_row = { order_keys[i]: text_prep(cells[i].text) for i in range(len(order_keys)) }
                        order_info.append(order_info_row)
                    print('order: ok')
                except:
                    print('order: -')

                try:
                    rows = soup.find('div', {'id': 'yw4_tab_3'}).find('div', {'id': 'yw0'}).find('tbody').find_all('tr')
                    manufacturer_info = []
                    for row in rows:
                        cells = row.find_all('td')
                        manufacturer_info_row = { manufacturer_keys[i]: text_prep(cells[i].text) for i in range(len(manufacturer_keys)) }
                        manufacturer_info.append(manufacturer_info_row)
                    print('manufacturer: ok')
                except:
                    print('manufacturer: -')

                try:
                    completenesses_info = []
                    rows = soup.find('div', {'id': 'yw4_tab_4'}).find('table').find_all('tr')[1:]
                    for row in rows:
                        cells = row.find_all('td')[:7]
                        completenesses_info_row = { completenesses_keys[i]: text_prep(cells[i].text) for i in range(len(completenesses_keys[:7]))}
                        completenesses_info.append(completenesses_info_row)
                    print('completenesses: ok')
                except:
                    print('completenesses: -')

                try: 
                    rows = soup.find('div', {'id': 'yw4_tab_5'}).find('table').find_all('tr')
                    variants_info = []
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) == 5:
                            variants_info_row = { variants_keys[i]: text_prep(cells[i].text) for i in range(len(variants_keys))}
                            variants_info_row_full = {**variants_info_row, 'activity': 'Есть'}
                            variants_info.append(variants_info_row_full)
                    print('variants: ok')
                except:
                    print('variants: -')

                try:
                    rows = soup.find('div', {'id': 'yw4_tab_6'}).find('div', {'id': 'yw1'}).find('tbody').find_all('tr')
                    instructions_info = []
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) > 1:
                            instructions_info_row = { instructions_keys[i]: 'http://register.ndda.kz' + cells[i].find('a')['href'] if cells[i].find('a') else text_prep(cells[i].text) for i in range(len(instructions_keys)) }
                            instructions_info.append(instructions_info_row)
                    print('instructions: ok')
                except:
                    print('instructions: -')

                try:
                    certificate_info = []
                    rows = soup.find('div', {'id': 'yw4_tab_7'}).find('table').find_all('tr')[1:]
                    for row in rows:
                        cells = row.find_all('td')
                        certificate_info_row = { certificate_keys[i]: text_prep(cells[i].text) for i in range(len(certificate_keys)) }
                        certificate_info.append(certificate_info_row)
                    print('certificate: ok')
                except:
                    print('certificate: -')

                try:
                    rows = soup.find('div', {'id': 'yw4_tab_8'}).find('div', {'id': 'yw2'}).find('tbody').find_all('tr')
                    package_info = []
                    for row in rows:
                        try:
                            cells = row.find_all('td')
                            name = text_prep(cells[0].text)
                            is_primary = True if cells[1].find('input',attrs={'name':'inner_sign'}).has_attr('checked') else False
                            
                            cells_rest = cells[2:]
                            package_info_row = { package_keys[i]: text_prep(cells_rest[i].text) for i in range(len(package_keys)) }
                            package_info_row_data = {
                                'name': name,
                                'primary': is_primary,
                                **package_info_row
                            }
                            package_info.append(package_info_row_data)
                        except:
                            package_info = []
                    print('package: ok')
                except:
                    print('package: -')
                        
                website = {
                    'name': 'ndda.kz mi',
                    'country': 'Казахстан'
                }

                # merge all subdata
                item = { 
                        'mainInfo': main_info, 
                        'decrees': order_info, 
                        'manufacturers': manufacturer_info, 
                        'completeness': completenesses_info,
                        'variants': variants_info,
                        'instructions': instructions_info, 
                        'certificates': certificate_info,
                        'packages': package_info, 
                        'nmirks': nmirks,
                        'website': website
                    }

                print('DONE')
                try:
                    # sending data by kafka
                    send_data(item)
                    # find close button and close current window
                    # driver.find_element_by_class_name('close').click()
                    # close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
                    # ActionChains(driver).move_to_element(close_button).click(close_button).perform()
                    # insert product item data into global data list and write to the file
                    # data.append(item)
                    data_counter += 1
                    # with open('data.json', 'w', encoding='utf-8') as f:
                        # json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f'LENGTH OF LIST: {data_counter}')
                    print(f'ORDER OF PRODUCT: {i + 1}')
                    print(f'CURRENT PAGE: {current_page}')
                    print()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(f'SMTH IS WORONG:\n{p_cells[2].text}')
                # driver.find_element_by_class_name('close').click()
                time.sleep(1)
                continue
        try:
            # go to the next page if possible; else break the loop
            print('---attempt to go to the next page---')
            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'next_register_pager'))).click()
        except:
            print('seems to be the end')
            state = 'reparsing'
        try: 
            # shit time sleep
            WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'load_register_grid')))
            # parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
        except:
            print('ah shit')
            time.sleep(10)

def bootstrap():
    while True:
        opts = webdriver.ChromeOptions()
        opts.add_argument("--window-size=1920,1080") 
        opts.add_argument("--headless")
        opts.add_argument("--disable-xss-auditor")
        opts.add_argument("--disable-web-security")
        opts.add_argument("--allow-running-insecure-content")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-setuid-sandbox")
        opts.add_argument("--disable-webgl")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument('--disable-dev-shm-usage') 

        PATH = chrome_path
        # PATH = '/Users/assanbekkaliyev/Desktop/chromedriver'
        driver = webdriver.Chrome(executable_path=PATH, options=opts)
        driver.get('http://register.ndda.kz/category/search_prep')

        frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "iframe1")))
        driver.switch_to.frame(frame)

        search_handler(driver)
        # sort by reg date
        table_check(driver, 'ui-row-ltr')
        toggle = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'jqgh_register_grid_reg_date')))
        ActionChains(driver).move_to_element(toggle).click(toggle).perform()
        # -----
        pagination_handler(driver, 1)
        table_check(driver, 'ui-row-ltr')
        try:
            process_parser(driver)
        except:
            global state
            state = 'not available'
            continue

bootstrap()