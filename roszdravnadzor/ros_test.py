from bs4 import BeautifulSoup
import requests

from shit_functions import *

headers = {
    'Date': 'Wed, 24 Nov 2021 06:51:15 GMT',
    'Strict-Transport-Security': 'max-age=31536000; includeSubdomains; preload',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin',
    'Content-Security-Policy': 'upgrade-insecure-requests;',
    'X-XSS-Protection': '1; mode=block',
    'Connection': 'close',
    'Transfer-Encoding': 'chunked',
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'roszdravnadzor.gov.ru',
    'Connection': 'keep-alive',
    'Content-Length': '4190',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'sec-ch-ua-platform': "macOS",
    'Origin': 'https://roszdravnadzor.gov.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://roszdravnadzor.gov.ru/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'uid=1726107303004960300; _ym_uid=1637736399807222886; _ym_d=1637736399; _ym_visorc=w; _ym_isad=2; sputnik_session=1637736399815|1'
}

def get_prod(start_year):
    return {
        'start': 0,
        'length': 10000,
        'search[value]': '',
        "dt_ru_from": f'01.01.{start_year}',
        "dt_ru_to": f'01.01.{start_year + 1}',
    }

def process_parser():
    for year in range(1985, 2022):
        try:
            r = requests.post('https://roszdravnadzor.gov.ru/ajax/services/misearch', headers=headers, params=get_prod(year))

            for index, item in enumerate(r.json()['data']):
                
                try: title = item['col5']['title'] 
                except: title = item['col5']['label']

                main_info = {
                    'type': 'МИ',
                    'registrationType': '',
                    'dosage': '',
                    'lsType': '',
                    'reg_number': item['col2']['label'] or '',
                    'registrationData': item['col3']['label'] or '',
                    'registrationExpireData': '',
                    'registrationLife': item['col4']['label'] or '',
                    'shelfLife': '',
                    'productName': title,
                    'appointment': item['col14']['label'] or '',
                    'fieldOfUse': '',
                    'securityClass': item['col13']['label'] or '',
                    'shortTechDescription': '',
                    'attributes': '',
                    'shelfLifeComment': ''
                }
                manufacturers = [{
                    'form': '',
                    'name': item['col9']['label'] or '' if item['col9']['label'] else item['col6']['label'] or '',
                    'nameInEnglish': '',
                    'country': '',
                    'type': ''
                }]
                website = {
                    'name': 'roszdravnadzor.gov.ru',
                    'country': 'Россия'
                }
                position = { 
                    'mainInfo': main_info, 
                    'decrees': [], 
                    'manufacturers': manufacturers, 
                    'completeness': [],
                    'variants': [],
                    'instructions': [], 
                    'certificates': [],
                    'packages': [], 
                    'nmirks': [],
                    'website': website
                }

                if position['mainInfo']['productName'] is None:
                    print('EMPTY PROD')
                else:
                    send_data(position)

                    print(f'{year} - {year + 1}')
                    print(f"DONE: {position['mainInfo']['productName']}")
                    print(f'TOTAL ON SECTION: {len(r.json()["data"])}')
                    print(f'ORDER OF PRODUCT: {index + 1}')
                    print(f"{year} / 2022")
            
        except Exception as e:
            print(e)
            continue
        finally:
            print()

while True:
    process_parser()