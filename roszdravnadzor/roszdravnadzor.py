from selenium import webdriver
from shit_functions import *
from shit_dict import *
from shit_chrome_path import *
import time

state = 'parsing'
data = []

def process_parser(driver):
    while True:
        try:
            WebDriverWait(driver, 300).until(EC.invisibility_of_element((By.ID, 'DataTables_Table_1_processing')))
            rows = wait_table(driver)
        except:
            # handle shit or change state
            global state
            state = 'not available'
            driver.close()
            print('smth is wrng')
            break

        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            position = {keys[index]: text_prep(cell) for index, cell in enumerate(cells)}

            main_info = {
                'type': 'МИ',
                'registrationType': '',
                'dosage': '',
                'lsType': '',
                'reg_number': position['reg_number'],
                'registrationData': position['reg_date'],
                'registrationExpireData': '',
                'registrationLife': position['validity'],
                'shelfLife': '',
                'productName': position['name'],
                'appointment': position['appointment_of_drugs'],
                'fieldOfUse': '',
                'securityClass': position['risk_class'],
                'shortTechDescription': '',
                'attributes': '',
                'shelfLifeComment': ''
            }

            manufacturers = [{
                'form': '',
                'name': position['name_of_applicant'],
                'nameInEnglish': '',
                'country': '',
                'type': ''
            }]

            website = {
                'name': 'roszdravnadzor.gov.ru',
                'country': 'Россия'
            }

            position = { 
                'mainInfo': main_info, 
                'decrees': [], 
                'manufacturers': manufacturers, 
                'completeness': [],
                'variants': [],
                'instructions': [], 
                'certificates': [],
                'packages': [], 
                'nmirks': [],
                'website': website
            }
            
            if position['mainInfo']['productName'] is None:
                # skip shit products wo prod name
                print('shit here')
                state = 'not available'
                break
            else:
                # data.append(position)
                print(position['mainInfo']['productName'], '\n')
                # print(len(data))
                # kafka send
                send_data(position)

            # with open('data.json', 'w', encoding='utf-8') as f:
                # json.dump(data, f, ensure_ascii=False, indent=4)

        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'DataTables_Table_1_next')))
            if 'disabled' not in next_button.get_attribute('class'):
                ActionChains(driver).move_to_element(next_button).click().perform()
                print('clicked')
                WebDriverWait(driver, 300).until(EC.invisibility_of_element((By.ID, 'DataTables_Table_1_processing')))
                rows = wait_table(driver)
            else: 
                print('disabled')
                print('seems to be finished')
                state = 'reparsing'
                break
        except Exception as e:
            print(e)
            break

def bootstrap():
    while True:
        print('1 sec timeout')
        time.sleep(1)

        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--disable-xss-auditor")
        opts.add_argument("--disable-web-security")
        opts.add_argument("--allow-running-insecure-content")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-setuid-sandbox")
        opts.add_argument("--disable-webgl")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--window-size=1920,1080")

        # PATH = chrome_path
        PATH = '/Users/assanbekkaliyev/Desktop/chromedriver'
        driver = webdriver.Chrome(PATH, options=opts)

        url = 'https://roszdravnadzor.gov.ru/services/misearch'
        # temp shit
        driver.get(url)
        for year in range(1999, 2022):
            # print(year)
            try:
                search_handler(driver, year)
                process_parser(driver)
            except:
                global state
                state = 'not available'
                pass

bootstrap()
        