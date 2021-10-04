from bs4 import BeautifulSoup
import requests
import json
from shit_dict import *

url = 'http://212.112.103.101'
reestr = url + '/reestr'

def get_data(reestr):
    source = requests.post(reestr, request_data).text
    return BeautifulSoup(source, 'lxml')

soup = get_data(reestr)

# working with the table body
body = soup.find('tbody')

data = []
for row in body.find_all('tr'):
    cells = row.find_all('td')
    name = row.select_one('td:nth-child(1)').text
    instruction = url + row.select_one('td:nth-child(2) > a:nth-child(1)')['href']

    temp_position = { position_keys[index]: cell.text for index, cell in enumerate(cells[2:]) }
    position = {'name': name, 'instruction': instruction, **temp_position}
    print(json.dumps(position, indent=2, ensure_ascii=False))
    data.append(position)
    print(len(data))
