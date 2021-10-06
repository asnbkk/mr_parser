from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from shit_functions import *

PATH = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH)
url = 'https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx'
driver.get(url)

new_driver(driver)

# while True:
table = driver.find_element_by_tag_name('tbody')
current_page = get_current_page_number(driver)

rows = table.find_elements_by_tag_name('tr')