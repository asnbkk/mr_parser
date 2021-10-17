from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from shit_chrome_path import *
from shit_functions import *
from shit_dict import *

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
url = 'https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx'
driver.get(url)

# new_driver(driver)
try:
    WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.XPATH, '//span[@data-bind="text: $data"]')))
except:
    # handle this shit
    print('problem w this site')

data = []
while True:
    rows = driver.find_elements_by_xpath('//table[@class="table"]/tbody[2]/tr')
    current_page = get_current_page_number(driver)

    for row in rows:
        try:
            time.sleep(5)
            product_click(row, driver)
            driver.switch_to.window(driver.window_handles[1])

            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'card3content')))

            name = driver.find_element_by_xpath('//div[@class="v-card__description"]/h2').text
            # print(name)

            table = driver.find_elements_by_xpath('//div[@id="zebra0"]/ul/li[@class="zebra-list__item"]')[1:4]
            instruction = table[-1].find_element_by_xpath('//div/ul/li/a[@class="link"]').get_attribute('href')
            # print(instruction)

            reg_data = { reg_data_keys[i]: text_prep(table[i].find_element_by_class_name('zebra-list__content').text) for i in range(len(reg_data_keys)) }
            reg_header = { 'name': name, **reg_data, 'instruction_link': instruction }

            # tab2
            tab2 = driver.find_element_by_xpath('//a[contains(text(), "Медицинское изделие")]')
            tab2.click()
            time.sleep(5)

            left_tree = driver.find_element_by_id('tab2tree')
            manufac_link = left_tree.find_element_by_xpath('//a[@title="Производитель"]').get_attribute('href').split('#')[-1]
            manufac = driver.find_elements_by_xpath(f'//div[@id="{manufac_link}"]/div/ul/li')

            manufacturer_list = []
            for i in range(0, 5, 2):
                manufacturer_list.append(text_prep(manufac[i].find_element_by_class_name('zebra-list__content').text))

            manufacturer_data = { manufacturer_keys[i]: manufacturer_list[i] for i in range(len(manufacturer_keys)) }
            manufacturer = { **manufacturer_data, 'manufacturer_country': manufacturer_list[-1].split(',')[0] }
        
        except:
            print('shit with prod')
            pass
        finally:
        # position = { **reg_header, **manufacturer }
        # print(len(data))
            main_info = {
                'type': '',
                'registrationType': '',
                'registrationData': reg_data['reg_date'],
                'registrationExpireData': reg_data['reg_end_date'],
                'registrationLife': '',
                'shelfLife': '',
                'productName': name,
                'appointment': '',
                'fieldOfUse': '',
                'securityClass': '',
                'shortTechDescription': '',
                'attributes': '',
                'shelfLifeComment': ''
            }

            manufacturers = {
                'form': manufacturer_data['form'],
                'name': manufacturer_data['manufacturer_name'],
                'nameInEnglish': '',
                'country': manufacturer_list[-1].split(',')[0],
                'type': ''
            }

            instructions = {
                'type': 'Инструкция по применению медицинского изделия',
                'comment': '',
                'fileInRussian': instruction,
                'fileInKazakh': ''
            }

            website = {
                'name': 'portal.eaeunion.org',
                'country': ''
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
            data.append(position)
            print(len(data))

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    try:
        next_page_button = driver.find_element_by_class_name('arrow-right').click()
        time.sleep(5)
        new_driver(driver, current_page)
    except: 
        print('this is the end!')
        break
