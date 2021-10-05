from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def new_driver(driver):
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'row_0.0')))
    except: 
        driver.quit()