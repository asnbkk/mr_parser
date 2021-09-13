from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = '/Users/assanbekkaliyev/Downloads/chromedriver'
driver = webdriver.Chrome(PATH)
# ебать мой хуй, это оказывается iframe. У него другая ссылка
driver.get('http://register.ndda.kz/register.php/mainpage/reestr/lang/ru')

def search_handler():
    try: 
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'ReestrTableForNdda_name')))
        search_input.click()
        search_input.send_keys(' ')
        search_input.submit()
    except Exception as e: 
        print(e)   


search_handler()


