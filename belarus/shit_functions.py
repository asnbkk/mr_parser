from shit_dict import * 
from bs4 import BeautifulSoup
import requests

def insert_page_index(index):
    return {'ValueSubmit': index, **request_data}

def get_data(reestr, index):
    request_data = insert_page_index(index)
    source = requests.post(reestr, request_data).text
    return BeautifulSoup(source, 'lxml')

def merge_all_data(dict1, dict2, manufacturing_country, instruction, type, appointment):
    return {
        **dict1, 
        **dict2, 
        'manufacturing_country': manufacturing_country, 
        'instruction': instruction, 
        'type': type, 
        'appointment': appointment
        }