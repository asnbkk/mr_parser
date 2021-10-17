from bs4 import BeautifulSoup
import requests
import json
from shit_dict import *
from shit_functions import *
import time

data = []
state = 'parsing'

def process_parser(url, reestr):
    soup = get_data(reestr)
    # working with the table body
    body = soup.find('tbody')
    try:
        for row in body.find_all('tr'):
            cells = row.find_all('td')
            name = row.select_one('td:nth-child(1)').text
            instruction = url + row.select_one('td:nth-child(2) > a:nth-child(1)')['href']

            main_info = {
                'type': '',
                'productName': name,
                'registrationType': '',
                'registrationData': cells[-2].text,
                'registrationLife': '',
                'registrationExpireData': '',
                'shelfLife': '',
                'appointment': '',
                'fieldOfUse': '',
                'securityClass': '',
                'shortTechDescription': '',
                'attributes': '',
                'shelfLifeComment': ''
            }

            manufacturers = [{
                'form': cells[3].text,
                'name': cells[6].text,
                'nameInEnglish': '',
                'country': cells[7].text,
                'type': ''
            }]

            instructions = [{
                'type': '',
                'comment': '',
                'fileInRussian': instruction,
                'fileInKazakh': ''
            }]

            website = {
                'name': 'kyrgyzstan',
                'country': ''
            }

            position = {
                'mainInfo': main_info,
                'decrees': [],
                'manufacturers': manufacturers,
                'completenesses': [],
                'variants': [],
                'instructions': instructions,
                'certificates': [],
                'packages': [], 
                'mnirk': [],
                'website': website
            }
            
            global state 
            state = 'reparsing'
            send_data(position)
            print(position['mainInfo']['productName'])
    except:
        state = 'not available'
        print('website is not working')

def get_data(reestr):
    source = requests.post(reestr, request_data).text
    return BeautifulSoup(source, 'lxml')

def bootstrap():
    while True:
        print('timer for 5 secs')
        time.sleep(5)
        url = 'http://212.112.103.101'
        reestr = url + '/reestr'
        
        try:
            print('starting parser')
            process_parser(url, reestr)
        except Exception as e:
            print(e)
            global state
            state = 'not available'
        
bootstrap()
