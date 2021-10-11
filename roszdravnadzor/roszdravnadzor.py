from selenium import webdriver
from shit_functions import *
from shit_dict import *
import time

PATH = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH)
url = 'https://roszdravnadzor.gov.ru/services/misearch'
driver.get(url)

search_handler(driver)

data = []

while True:
    rows = wait_table(driver)
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        position = {keys[index]: text_prep(cell.text) for index, cell in enumerate(cells)}
        data.append(position)
        print(position['reg_number'])
        print(len(data))

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # kafka send
        send_data(position)

    try:
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'DataTables_Table_1_next'))).click()
    except Exception as e:
        print(e)
        print('seems to be finished')
        break
    
    try: 
        WebDriverWait(driver, 300).until(EC.invisibility_of_element((By.ID, 'DataTables_Table_1_processing')))
        rows = wait_table(driver)
    except:
        print('ah shit')
        time.sleep(10)

    