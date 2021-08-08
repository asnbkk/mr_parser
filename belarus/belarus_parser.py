from bs4 import BeautifulSoup
import requests

url = 'https://www.rceth.by'
reestr = url + '/Refbank/reestr_medicinskoy_tehniki/results'

def get_data(reestr, index):
    source = requests.post(
        reestr, data={
                'QueryStringFind': 'Rk9wdC5WQW5bPV1GYWxzZVs7XUZPcHQuVlVuVGVybVs9XUZhbHNlWztdRk9wdC5WUGF1c2VbPV1GYWxzZVs7XUZPcHQuVkZpbGVzWz1dVHJ1ZVs7XUZPcHQuVkVGaWVsZDFbPV1GYWxzZVs7XUZPcHQuT3JkZXJCeVs9XVByb2R1Y3ROYW1lWztdRk9wdC5EaXJPcmRlcls9XWFzY1s7XUZPcHQuVlRbPV10WztdRk9wdC5QYWdlQ1s9XTEwMFs7XUZPcHQuUGFnZU5bPV0xWztdRk9wdC5DUmVjWz1dMTk3NzZbO11GT3B0LkNQYWdlWz1dMTk4WztdRlByb3BzWzBdLk5hbWVbPV1Qcm9kdWN0TmFtZVs7XUZQcm9wc1swXS5Jc1RleHRbPV1UcnVlWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5WYWxbPV0gWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5FeGNsWz1dRmFsc2VbO11GUHJvcHNbMF0uQ3JpdEVsZW1zWzBdLkNyaXRbPV1MaWtlWztdRlByb3BzWzBdLkNyaXRFbGVtc1swXS5OdW1bPV0xWztdRlByb3BzWzFdLk5hbWVbPV1UeXBlWztdRlByb3BzWzFdLklzRHJvcFs9XVRydWVbO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLlZhbFs9XV9bO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLkV4Y2xbPV1GYWxzZVs7XUZQcm9wc1sxXS5Dcml0RWxlbXNbMF0uQ3JpdFs9XUxpa2VbO11GUHJvcHNbMV0uQ3JpdEVsZW1zWzBdLk51bVs9XTFbO11GUHJvcHNbMl0uTmFtZVs9XU1hbnVmYWN0dXJlcls7XUZQcm9wc1syXS5Jc1RleHRbPV1UcnVlWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5WYWxbPV1fWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5FeGNsWz1dRmFsc2VbO11GUHJvcHNbMl0uQ3JpdEVsZW1zWzBdLkNyaXRbPV1MaWtlWztdRlByb3BzWzJdLkNyaXRFbGVtc1swXS5OdW1bPV0xWztdRlByb3BzWzNdLk5hbWVbPV1EZWNsYXJhbnRbO11GUHJvcHNbM10uSXNUZXh0Wz1dVHJ1ZVs7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uVmFsWz1dX1s7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uRXhjbFs9XUZhbHNlWztdRlByb3BzWzNdLkNyaXRFbGVtc1swXS5Dcml0Wz1dTGlrZVs7XUZQcm9wc1szXS5Dcml0RWxlbXNbMF0uTnVtWz1dMVs7XUZQcm9wc1s0XS5OYW1lWz1dQ2VydGlmaWNhdGVOdW1iZXJbO11GUHJvcHNbNF0uSXNUZXh0Wz1dVHJ1ZVs7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uVmFsWz1dX1s7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uRXhjbFs9XUZhbHNlWztdRlByb3BzWzRdLkNyaXRFbGVtc1swXS5Dcml0Wz1dTGlrZVs7XUZQcm9wc1s0XS5Dcml0RWxlbXNbMF0uTnVtWz1dMVs7XUZQcm9wc1s1XS5OYW1lWz1dQ2VydGlmaWNhdGVEYXRlWztdRlByb3BzWzVdLklzRGF0ZVs9XVRydWVbO11GUHJvcHNbNV0uQ3JpdEVsZW1zRC5WYWwxWz1dbnVsbFs7XUZQcm9wc1s1XS5Dcml0RWxlbXNELlZhbDJbPV1udWxsWztdRlByb3BzWzVdLkNyaXRFbGVtc0QuQ3JpdFs9XUVxdWFsWztdRlByb3BzWzZdLk5hbWVbPV1UZXJtWztdRlByb3BzWzZdLklzRGF0ZVs9XVRydWVbO11GUHJvcHNbNl0uQ3JpdEVsZW1zRC5WYWwxWz1dbnVsbFs7XUZQcm9wc1s2XS5Dcml0RWxlbXNELlZhbDJbPV1udWxsWztdRlByb3BzWzZdLkNyaXRFbGVtc0QuQ3JpdFs9XUVxdWFsWztd',
                'IsPostBack': 'True',
                'PropSubmit': 'FOpt_PageN',
                'ValueSubmit': f'{index}',
                'VFiles': 'True',
                'FProps[0].IsText': 'True',
                'FProps[0].Name': 'ProductName',
                'FProps[0].CritElems[0].Num': '1',
                'FProps[0].CritElems[0].Val':  ' ',
                'FProps[0].CritElems[0].Crit': 'Like',
                'FProps[0].CritElems[0].Excl': 'false',
                'FProps[1].IsDrop': 'True',
                'FProps[1].Name': 'Type',
                'FProps[1].CritElems[0].Num': '1',
                'FProps[1].CritElems[0].Val': '',
                'FProps[1].CritElems[0].Excl': 'false',
                'FProps[2].IsText': 'True',
                'FProps[2].Name': 'Manufacturer',
                'FProps[2].CritElems[0].Num': '1',
                'FProps[2].CritElems[0].Val': '',
                'FProps[2].CritElems[0].Crit': 'Like',
                'FProps[2].CritElems[0].Excl': 'false',
                'FProps[3].IsText': 'True',
                'FProps[3].Name': 'Declarant',
                'FProps[3].CritElems[0].Num': '1',
                'FProps[3].CritElems[0].Val': '',
                'FProps[3].CritElems[0].Crit': 'Like',
                'FProps[3].CritElems[0].Excl': 'false',
                'FProps[4].IsText': 'True',
                'FProps[4].Name': 'CertificateNumber',
                'FProps[4].CritElems[0].Num': '1',
                'FProps[4].CritElems[0].Val': '',
                'FProps[4].CritElems[0].Crit': 'Like',
                'FProps[4].CritElems[0].Excl': 'false',
                'FProps[5].IsDate': 'True',
                'FProps[5].Name': 'CertificateDate',
                'FProps[5].CritElemsD.Val1': '',
                'FProps[5].CritElemsD.Crit': 'Equal',
                'FProps[6].IsDate': 'True',
                'FProps[6].Name': 'Term',
                'FProps[6].CritElemsD.Val1': '',
                'FProps[6].CritElemsD.Crit': 'Equal',
                'FOpt.PageC': '100',
                'FOpt.OrderBy': 'ProductName',
                'FOpt.DirOrder': 'asc',
                'FOpt.VFiles': 'true',
                'FOpt.VFiles': 'false',
        }).text

    return BeautifulSoup(source, 'lxml')

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

    name = table.select_one('td:nth-child(1)').text.strip()
    print(f'Название: {name}')

    vendor = table.select_one('td:nth-child(2)').text.strip()
    print(f'Код, артикул: {vendor}')

    manufacturing_company = table.select_one('td:nth-child(3)') \
        .contents[0].strip()
    print(f'Производитель: {manufacturing_company}')

    production_site = table.select_one('td:nth-child(4)').text.strip()
    print(f'Производственная площадка: {production_site}')

    applicant = table.select_one('td:nth-child(5)').text.strip()
    print(f'Заявитель: {applicant}')

    manufacturing_country = applicant.split(', ')[-1].capitalize()
    print(f'Страна производства: {manufacturing_country}')

    try: 
        instruction = url + table.select_one('td:nth-child(6)') \
            .find('a')['href']
    except: instruction = None
    print(f'Инструкция: {instruction}')

    certificates_no = table.select_one('td:nth-child(6)').contents[0].strip()
    print(f'Номер удостоверения: {certificates_no}')

    reg_item_number = table.select_one('td:nth-child(7)').text.strip()
    print(f'Рег. номер товара: {reg_item_number}')

    reg_date = table.select_one('td:nth-child(8)').text.strip()
    print(f'Дата регистрации: {reg_date}')

    validity = table.select_one('td:nth-child(9)').text.strip()
    print(f'Срок действия: {validity}')

    type = add_table.select_one('tr:nth-child(1)') \
            .select_one('td:nth-child(2)').text.strip().capitalize()
    print(f'Тип: {type}')

    appointment = add_table.select_one('tr:nth-child(2)') \
            .select_one('td:nth-child(2)').text.strip()
    print(f'Назначение: {appointment}')

    print('--------------------------------')
    print()

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