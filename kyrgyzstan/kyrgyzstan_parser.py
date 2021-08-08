from bs4 import BeautifulSoup
import requests
import csv

url = 'http://212.112.103.101'
reestr = url + '/reestr'


def get_data(reestr):
    source = requests.post(
        reestr, data={'name': '',
                      'mnn': '',
                      'proizvod': '%%%',
                      'ftg': '',
                      'ath': '',
                      'ean': ''}).text

    soup = BeautifulSoup(source, 'lxml')
    return soup


soup = get_data(reestr)

# working with the table body
body = soup.find('tbody')
for row in body.find_all('tr'):

    name = row.select_one('td:nth-child(1)').text
    instruction = url + \
        row.select_one('td:nth-child(2) > a:nth-child(1)')['href']
    mnn = row.select_one('td:nth-child(3)').text
    dosage_form = row.select_one('td:nth-child(4)').text
    dosage = row.select_one('td:nth-child(5)').text
    packing = row.select_one('td:nth-child(6)').text
    manufacturing_company = row.select_one('td:nth-child(7)').text
    manufacturing_country = row.select_one('td:nth-child(8)').text
    certificate_holder = row.select_one('td:nth-child(9)').text
    certificate_holder_country = row.select_one('td:nth-child(10)').text
    atx = row.select_one('td:nth-child(11)').text
    pharma_group = row.select_one('td:nth-child(12)').text
    life_saving_medication = row.select_one('td:nth-child(13)').text
    terms_of_dispensing = row.select_one('td:nth-child(14)').text
    certificates_no = row.select_one('td:nth-child(15)').text
    date_of_issue = row.select_one('td:nth-child(16)').text
    ean = row.select_one('td:nth-child(17)').text

    print('----------------------')
    print('Наименование: ', name)
    print('Инструкция: ', instruction)
    print('МНН: ', mnn)
    print('Лекарственная форма: ', dosage_form)
    print('Дозировка: ', dosage)
    print('Фасовка: ', packing)
    print('Предприятие производитель: ', manufacturing_company)
    print('Страна производства: ', manufacturing_country)
    print('Держатель свидетельства: ', certificate_holder)
    print('Страна держателя свидетельства: ', certificate_holder_country)
    print('АТХ: ', atx)
    print('Фармакотерапевтическая группа: ', pharma_group)
    print('ПЖВЛС: ', life_saving_medication)
    print('Условия отпуска из аптек: ', terms_of_dispensing)
    print('№ свидетельства: ', certificates_no)
    print('Дата выдачи: ', date_of_issue)
    print('EAN13: ', ean)
