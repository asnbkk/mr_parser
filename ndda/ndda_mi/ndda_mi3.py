from os import DirEntry, stat
from selenium import webdriver
from shit_dict import *
from shit_methods import *
from shit_chrome_path import *
import time
# import json

state = 'parsing'
data = []

# page_amount = int(driver.find_element_by_id('sp_1_register_pager').text)
# for page in range(page_amount):
def process_parser(driver):
    while True:
        try:
            parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
        except:
            global state
            state = 'not available'
            break
        
        for index, row in enumerate(parent_rows):
            try:
                try:
                    cells = parent_rows[index].find_elements_by_tag_name('td')
                    attributes = cells[15:21]
                    reg_number = cells[0]
                    attributes_list = []
                except Exception as e:
                    print(e)

                for index, attr in enumerate(attributes):
                        if attr.find_element_by_tag_name('input').get_attribute('checked') == 'true':
                            attributes_list.append(attributes_keys[index])
                # new item open

                link = WebDriverWait(row, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'openReestr')))
                ActionChains(driver).move_to_element(link).click(link).perform()

                table_check(driver, 'modal-open')
                main_table = WebDriverWait(driver, 5).until(
                    EC.visibility_of_all_elements_located((By.XPATH, '//form[@id="reestr-form-reestrForm-form"]//tbody//td')))[1::2]

                # main_table = driver.find_elements_by_xpath('//form[@id="reestr-form-reestrForm-form"]//tbody//td')[1::2]
                general_info_rows = main_table[:11]

                attributes = cells[15:21]
                attributes_list = []
                
                general_info = {general_info_keys[i]: text_prep(general_info_rows[i].text) for i in range(len(general_info_keys))}
                main_info = {
                    **general_info, 
                    'reg_number': text_prep(reg_number.text),
                    'shelfLifeComment': text_prep(main_table[-2].text), 
                    'attributes': ','.join(attributes_list),
                    'dosage': '',
                    'lsType': ''}

                secondary_table = driver.find_element_by_xpath('//table[@class="table table-bordered table-hover"]')
                secondary_table_rows = secondary_table.find_elements_by_tag_name('tr')[1:]
                nmirks = []
                for row in secondary_table_rows:
                    cells = row.find_elements_by_tag_name('td')
                    nmirk = {nmirk_keys[i]: text_prep(cells[i].text) for i in range(len(nmirk_keys))}
                    nmirks.append(nmirk)
            

                next_tab(driver, 0) 
                rows = wait_table(driver, 0, True)
                order_info = []

                for index, row in enumerate(rows):
                    cells = rows[index].find_elements_by_tag_name('td')
                    order_info_row = { order_keys[i]: text_prep(cells[i].text) for i in range(len(order_keys)) }
                    order_info.append(order_info_row)
                
                next_tab(driver, 1)
                rows = wait_table(driver, 1, False)
                manufacturer_info = []
                for index, row in enumerate(rows):
                    cells = row.find_elements_by_tag_name('td')
                    manufacturer_info_row = { manufacturer_keys[i]: text_prep(cells[i].text) for i in range(len(manufacturer_keys)) }
                    manufacturer_info.append(manufacturer_info_row)

                next_tab(driver, 2)
                rows = wait_table(driver, 2, True)
                completenesses_info = []
                for index, row in enumerate(rows):
                    # remove :7
                    cells = rows[index].find_elements_by_tag_name('td')[:7]
                    completenesses_info_row = { completenesses_keys[i]: text_prep(cells[i].text) for i in range(len(completenesses_keys[:7]))}
                    print(len(completenesses_info))
                    completenesses_info.append(completenesses_info_row)

                next_tab(driver, 3)
                rows = driver.find_elements_by_xpath('//div[@id="yw4_tab_5"]//tbody//tr')[1:]
                variants_info = []
                time.sleep(0.5)
                for index, row in enumerate(rows):
                    if row.text:
                        cells = rows[index].find_elements_by_tag_name('td')
                        variants_info_row = { variants_keys[i]: text_prep(cells[i].text) for i in range(len(variants_keys))}
                        variants_info_row_full = {**variants_info_row, 'activity': 'Есть'}
                        variants_info.append(variants_info_row_full)

                next_tab(driver, 4)
                rows = wait_table(driver, 4, False)
                instructions_info = []
                for index, row in enumerate(rows):
                    cells = rows[index].find_elements_by_tag_name('td')
                    # if cells[0].get_attribute('class') != 'empty':
                    if len(cells) > 1:
                        instructions_info_row = { instructions_keys[i]: text_prep(cells[i].text) if len(get_child(cells[i])) == 0 else get_child(cells[i])[0].get_attribute('href') for i in range(len(instructions_keys)) }
                        instructions_info.append(instructions_info_row)
                
                next_tab(driver, 5)
                rows = wait_table(driver, 5, True)
                certificate_info = []
                for index, row in enumerate(rows):
                    cells = rows[index].find_elements_by_tag_name('td')
                    certificate_info_row = { certificate_keys[i]: text_prep(cells[i].text) for i in range(len(certificate_keys)) }
                    certificate_info.append(certificate_info_row)

                next_tab(driver, 6)
                rows = wait_table(driver, 6, False, True)
                package_info = []
                for index, row in enumerate(rows):
                    try:
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
                    except:
                        package_info = []
                        
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

                print(item['mainInfo']['productName'])
                # sending data by kafka
                send_data(item)
                
                # find close button and close current window
                driver.find_element_by_class_name('close').click()

                # insert product item data into global data list and write to the file
                # data.append(item)
                # with open('data.json', 'w', encoding='utf-8') as f:
                #         json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print('im here you motherfucker')
                driver.find_element_by_class_name('close').click()
                # print(e)
                pass
        try:
            # go to the next page if possible; else break the loop
            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'next_register_pager'))).click()
        except:
            print('seems to be the end')
            state = 'reparsing'
            break
        try: 
            # shit time sleep
            WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'load_register_grid')))
            parent_rows = driver.find_elements_by_class_name('ui-row-ltr')
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

        PATH = chrome_path
        driver = webdriver.Chrome(PATH, options=opts)
        driver.get('http://register.ndda.kz/category/search_prep')

        frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "iframe1")))
        driver.switch_to.frame(frame)

        search_handler(driver)
        # sort by reg date
        table_check(driver, 'ui-row-ltr')
        toggle = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'jqgh_register_grid_reg_date')))
        ActionChains(driver).move_to_element(toggle).click(toggle).perform()
        # -----
        pagination_handler(driver, 60)
        table_check(driver, 'ui-row-ltr')
        try:
            process_parser(driver)
        except:
            global state
            state = 'not available'
            pass

bootstrap()