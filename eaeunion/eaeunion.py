# TODO:
# - modify dummy data
# - get panel[1:3] with clicks
# - merge all existing dicts
# - set pagination

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

# install selenium
# need to get the path of chromedriver
PATH = '/Users/assanbekkaliyev/Downloads/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get('https://portal.eaeunion.org/sites/commonprocesses/ru-ru/Pages/DrugRegistrationDetails.aspx')

try: 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'row_0.0')))
except: 
    # handle shit
    driver.quit()

table = driver.find_element_by_tag_name('tbody')
rows = table.find_elements_by_tag_name('tr')

for index, row in enumerate(rows):
    cells = row.find_elements_by_tag_name('td')

    header = cells[0].text
    mnn = cells[1].text

    release_form_list = []
    for item in cells[2].find_elements_by_tag_name('li'):
        release_form_list.append(item.text.replace('\n', ' '))

    manufacturer = cells[3].text

    char_of_med_product = []
    for item in cells[4].find_elements_by_tag_name('li'):
        char_of_med_product.append(item.text.replace('\n', ' '))

    # dummy print
    # print(f'name: {header}')
    # print(f'mnn: {mnn}')
    # print(f'release_form: {release_form_list}')
    # print(f'manufacturer: {manufacturer}')
    # print(f'char_of_med_product: {char_of_med_product}')

    actionChains = ActionChains(driver)
    actionChains.double_click(row).perform()

    # details
    driver.switch_to.window(driver.window_handles[1])
    try: 
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'flag-icon')))

        # data from panel1 list
        panel1_list = driver.find_elements_by_xpath("//div[@id='panel1']//ul//li")
        panel1_keys = ['be_name', 
                'be_brief_name', 
                'be_type', 
                'country', 
                'reg_address', 
                'e_location', 
                'postal_address', 
                'phone', 
                'email']

        panel1 = { panel1_keys[i]: panel1_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(panel1_keys)) }
        # print(panel1)

        # registration full data
        reg_data_list = driver.find_elements_by_xpath("//div[@id='registrations-list']//div[@class='zebra-list']//ul//li")
        reg_data_keys = ['reg_num', 'reg_status', 'reg_date']

        toggle_button = driver.find_element_by_class_name('product-list__trigger-icon').click()
        time.sleep(2)
        
        reg_data = { reg_data_keys[i]: reg_data_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(reg_data_keys)) }
        # print(reg_data)

        # list of left tabs
        tabs = driver.find_elements_by_xpath("//div[@class='left-menu__list']//ul//li")

        # get data from panel 2
        tabs[1].click()
        time.sleep(2)
        # md is medicinal product
        panel2_list = driver.find_elements_by_xpath("//div[@id='panel2']//ul//li")
        panel2_keys = [
            'ainternational_name', 
            'atx', 
            'pharmacy_type', 
            'additional_sign_of_md', 
            'pharm_form', 
            'conditions_for_dispending_md', 
            'classification_of_orphan_drugs']

        panel2 = { panel2_keys[i]: panel2_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(panel2_keys)) }
        # print(panel2)

        # get data from panel 4
        panel4_table_row = driver.find_elements_by_xpath("//div[@id='panel4']//tbody//tr")
        panel4 = []
        panel4_keys = [
            'dosage_form_and_dosage',
            'composition',
            'shelf_life',
            'primary_packaging',
            'accessories'
        ]
        for index, row in enumerate(panel4_table_row[1:], 1):
            table_row = row.find_elements_by_xpath(f"//tr/following-sibling::tr[{index}]//td")[2:]
            row = { panel4_keys[i]: table_row[i + 1].text for i in range(len(panel4_keys)) }
            panel4.append(row)
        # panel4 is array of dicts
        # print(panel4)

        # manufacturings-list toggle button
        tabs[2].click()
        time.sleep(2)

        manufacturings_list = []
        product_manufacturings_keys = [
                        'organizational_and_legal_form',
                        'country_of_registration_of_the_manufacturer',
                        'registration_address',
                        'place_of_business',
                        'mailing_address',
                        'telephone',
                        'email',
                        'fax'
                    ]
        production_sites_keys = [
                'production_stage',
                'production_site_name',
                'production_site_address',
                'contact_details'
            ]

        product_list = driver.find_elements_by_xpath("//div[@id='manufacturings-list']//ul//li[@class='product-list__item']")

        for index, product_item in enumerate(product_list):
            # open new tab
            product_list[index].find_element_by_class_name('product-list__trigger-icon').click()
            time.sleep(1)
            product_manufacturings_list = product_list[index].find_elements_by_class_name('zebra-list__item')
            manufacturings_row = { product_manufacturings_keys[i]: product_manufacturings_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(product_manufacturings_keys)) }
            # production sites
            production_sites_list = product_list[index].find_elements_by_class_name('table__cell')[4:]
            production_sites_row = { production_sites_keys[i]: production_sites_list[i].text for i in range(len(production_sites_keys)) }

            # merging tow intermediate dicts and appending to list
            manufacturings_list.append({**manufacturings_row, **production_sites_row})

        # print(manufacturings_list)

        # regulations toggle button
        tabs[3].click()
        time.sleep(2)

        regulations = []
        regulations_keys = [
            'document_name',
            'document_validity_period',
            'country'
        ]

        regulations_table_rows = driver.find_elements_by_xpath("//div[@id='panel5']//tbody//tr")[1:]
        for regulations_table_row in regulations_table_rows:
            table_cell = regulations_table_row.find_elements_by_class_name('table__cell')

            regulations_row_text = { regulations_keys[i]: table_cell[i].text for i in range(len(regulations_keys)) }
            document_link = { 'document_link': regulations_table_row.find_element_by_class_name('link').get_attribute('href') }
            # merging tow intermediate dicts and appending to list
            regulations_row = {**regulations_row_text, **document_link}
            regulations.append(regulations_row)
        # print(regulations)

        # pharmaceutical substances
        

    except Exception as e: 
        # handle shit
        print(e)
        print('next page is closed')
        # driver.switch_to.window(driver.window_handles[0])
    finally: 
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # panel_1 = driver.find_element_by_id('panel1')

    # print('-----------------')
    

driver.quit()