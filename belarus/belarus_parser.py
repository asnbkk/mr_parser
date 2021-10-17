from bs4 import BeautifulSoup
import requests
from shit_functions import *
from shit_dict import *
import json
import time

state = 'parsing'

url = 'https://www.rceth.by'
reestr = url + '/Refbank/reestr_medicinskoy_tehniki/results'

# get detailed data
def get_details(url, prod):
    detail = requests.get(url + prod * 2).text
    soup = BeautifulSoup(detail, 'lxml')

    table = soup \
        .find('div', {'class': 'table-view'}) \
        .find('tbody') \
        .find('tr')

    add_table = soup \
        .find('div', {'class': 'row-view'}) \
        .find('tbody')

    dict1 = {index[0]: table.select_one(f'td:nth-child({index[1]})').text.strip() for index in dict_1}
    dict2 = {index[0]: table.select_one(f'td:nth-child({index[1]})').contents[0].strip() for index in dict_2}
    manufacturing_country = dict1['applicant'].split(', ')[-1].capitalize()
    try: 
        instruction = url + table.select_one('td:nth-child(6)').find('a')['href']
    except: 
        instruction = None
    type = add_table.select_one('tr:nth-child(1)') \
            .select_one('td:nth-child(2)').text.strip().capitalize()
    appointment = add_table.select_one('tr:nth-child(2)') \
            .select_one('td:nth-child(2)').text.strip()

    position = merge_all_data(dict1, dict2, manufacturing_country, instruction, type, appointment)

    main_info = {
        'type': position['type'],
        'productName': position['name'],
        'registrationType': '',
        'registrationData': position['reg_date'],
        'registrationLife': '',
        'registrationExpireData': position['validity'],
        'shelfLife': '',
        'appointment': position['appointment'],
        'fieldOfUse': '',
        'securityClass': '',
        'shortTechDescription': '',
        'attributes': '',
        'shelfLifeComment': ''
    }

    manufacturers = [{
        'form': '',
        'name': position['manufacturing_company'],
        'nameInEnglish': '',
        'country': position['manufacturing_country'],
        'type': ''
    }]

    instructions = [{
        'type': 'Руководство по эксплуатации',
        'comment': '',
        'fileInRussian': position['instruction'],
        'fileInKazakh': ''
    }]

    certificates = [{
        'type': position['certificates_no'],
        'name': '',
        'dates': '',
        'organ': ''
    }]

    website = {
        'name': 'rceth.by',
        'country': ''
    }

    position = { 
        'mainInfo': main_info, 
        'decrees': [], 
        'manufacturers': manufacturers, 
        'completeness': [],
        'variants': [],
        'instructions': instructions, 
        'certificates': certificates,
        'packages': [], 
        'nmirks': [],
        'website': website
    }

    send_data(position)
    print(position['mainInfo']['productName'])

def bootstrap():
    i = 1
    while True:
        print('timer for 5 secs')
        time.sleep(5)

        soup = get_data(reestr, i)
        try: 
            global state
            table = soup \
                .find('div', {'class': 'table-view'}) \
                .find('tbody')
        except: 
            print('ITS OVEER!!!!')
            state = 'reparsing'
            pass
            
        # getting link for complex information
        try:
            for row in table.find_all('tr'):
                link = row.select_one('td:nth-child(2) > a')['href']
                get_details(url, link)
            i += 1
        except:
            state = 'not available'
            pass
bootstrap()