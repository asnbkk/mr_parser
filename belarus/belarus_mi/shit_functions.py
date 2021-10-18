from shit_dict import * 
from bs4 import BeautifulSoup
import requests

from shit_chrome_path import *
import json
from kafka import KafkaProducer

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

producer = KafkaProducer(
    bootstrap_servers=[kafka_host],
    api_version=(0,10,1),
    value_serializer=lambda x: 
    json.dumps(x).encode('utf-8')
    )

def send_data(data):
    producer.send('testTopic', value=data)