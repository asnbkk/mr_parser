from bs4 import BeautifulSoup
import requests
from shit_functions import *
from shit_dict import *

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
    print(position)

# move through multiple pages
i = 1
while True:
    soup = get_data(reestr, i)
    try: 
        table = soup \
            .find('div', {'class': 'table-view'}) \
            .find('tbody')
    except: 
        print('ITS OVEER!!!!')
        break

    # getting link for complex information
    for row in table.find_all('tr'):
        link = row.select_one('td:nth-child(2) > a')['href']
        get_details(url, link)
    i += 1