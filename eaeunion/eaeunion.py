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
    print(f'name: {header}')
    print(f'mnn: {mnn}')
    print(f'release_form: {release_form_list}')
    print(f'manufacturer: {manufacturer}')
    print(f'char_of_med_product: {char_of_med_product}')

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
        print(panel1)

        # registration full data
        reg_data_list = driver.find_elements_by_xpath("//div[@id='registrations-list']//div[@class='zebra-list']//ul//li")
        reg_data_keys = ['reg_num', 'reg_status', 'reg_date']

        toggle_button = driver.find_element_by_class_name('product-list__trigger-icon')
        toggle_button.click()

        time.sleep(5)
        
        reg_data = { reg_data_keys[i]: reg_data_list[i].find_element_by_class_name('zebra-list__content').text for i in range(len(reg_data_keys)) }
        print(reg_data)

        # get data from panel 2

    
    except: 
        # handle shit
        print('next page is closed')
        # driver.switch_to.window(driver.window_handles[0])
    finally: 
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # panel_1 = driver.find_element_by_id('panel1')

    print('-----------------')
    

driver.quit()