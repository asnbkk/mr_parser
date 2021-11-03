from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from shit_functions import *
from shit_dict import *

state = 'parsing'

# data = []

def process_parser(driver):
    current_page = 1
    while True:
        for index in range(100):
            parent_rows = WebDriverWait(driver, 300).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="results"]//tbody//tr')))

            cells = parent_rows[index].find_elements_by_tag_name('td')

            cell = cells[1].find_element_by_tag_name('a')
            open_prod(cell, driver)
            
            # primary table info
            try:
                primary_table_cells = WebDriverWait(driver, 300).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="table-view"]//tbody//tr//td')))

                primary_table = {primary_table_keys[i]: primary_table_cells[i].text for i in range(9)}

                instruction_name = primary_table_cells[-1].text
                instruction_link = primary_table_cells[-1].find_element_by_tag_name('a').get_attribute('href') if instruction_name != '' else ''

                secondary_table_cells = driver.find_elements_by_xpath('//div[@class="row-view"]//tbody//tr//td/following-sibling::td[1]')
                
                secondary_table = {secondary_table_keys[i]: secondary_table_cells[i].text for i in range(18)}

                main_info = {
                        'lsType': primary_table['type'],
                        'type': 'ЛС',
                        'dosage': '',
                        'registrationType': '',
                        'registrationData': primary_table['reg_date'],
                        'registrationExpireData': primary_table['reg_validity'],
                        'registrationLife': '',
                        'shelfLife': secondary_table['shelf_life'],
                        'productName': primary_table['name'],
                        'appointment': '',
                        'fieldOfUse': '',
                        'securityClass': '',
                        'shortTechDescription': '',
                        'attributes': '',
                        'shelfLifeComment': ''
                    }

                manufacturers = [{
                        'form': '',
                        'name': secondary_table['manufacturer'],
                        'nameInEnglish': '',
                        'country': '',
                        'type': ''
                    }]

                instructions = [{
                        'type': instruction_name,
                        'comment': '',
                        'fileInRussian': instruction_link,
                        'fileInKazakh': ''
                    }]

                website = {
                    'name': 'rceth.by',
                    'country': 'Беларусь'
                }

                position = { 
                    'mainInfo': main_info, 
                    'decrees': [], 
                    'manufacturers': manufacturers, 
                    'completeness': [],
                    'variants': [],
                    'instructions': instructions, 
                    'certificates': [],
                    'packages': [], 
                    'nmirks': [],
                    'website': website
                }

                send_data(position)
                # data.append(position)
                print(position['mainInfo']['productName'])

                # with open('data.json', 'w', encoding='utf-8') as f:
                    # json.dump(data, f, ensure_ascii=False, indent=4)

            except:
                print('smth wrng w prod')
                pass
            finally:
                driver.back()
        try:
            print(f'current page is {current_page}')
            pagination(current_page, driver)
            current_page += 1
        except:
            print('seems to be the end')
            break
    
def bootstrap():
    while True:
        print('timer for 3 secs')
        time.sleep(3)
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--disable-xss-auditor")
        opts.add_argument("--disable-web-security")
        opts.add_argument("--allow-running-insecure-content")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-setuid-sandbox")
        opts.add_argument("--disable-webgl")
        opts.add_argument("--disable-popup-blocking")

        PATH = chrome_path
        driver = webdriver.Chrome(PATH, options=opts)
        url = 'https://www.rceth.by/Refbank/reestr_lekarstvennih_sredstv/results'
        driver.get(url)

        search_handler(driver)
        try:
            process_parser(driver)
        except Exception as e:
            print(e)
            global state
            state = 'not available'
            pass

bootstrap()