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

# def new_driver():
#     try: 
#         WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'reestr-form-reestrForm-form')))

#         print(element)
#     except Exception as e: 
#         print(e)   


# new_driver()


