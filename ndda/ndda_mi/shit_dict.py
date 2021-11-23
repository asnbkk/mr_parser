headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1787853804.1631553712; PHPSESSID=03c060shssbrcjec4u3ksmbqo2; _gid=GA1.2.797183319.1637678990',
    'Host': 'register.ndda.kz',
    'Referer': 'http://register.ndda.kz/register.php/mainpage/reestr/lang/ru',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

general_info_keys = [
    'type',
    'registrationType',
    'registrationData',
    'registrationLife',
    'registrationExpireData',
    'shelfLife',
    'productName',
    'appointment',
    'fieldOfUse',
    'securityClass',
    'shortTechDescription'
]

nmirk_keys = [
    'code',
    'name',
    'description'
]

completenesses_keys = [
    'number',
    'name',
    'nameInKazakh',
    'typeOfParts',
    'typeOfPartsKazakh',
    'model',
    'modelKazakh',
    'manufacturer',
    'manufacturerInKazakh',
    'countries',
    'countriesInKazakh'
]

tab_list = [
    'yw4_tab_2',
    'yw4_tab_3',
    'yw4_tab_4',
    'yw4_tab_5',
    'yw4_tab_6',
    'yw4_tab_7',
    'yw4_tab_8'
]

order_keys = [
    'number',
    'date',
    'type',
    'comment'
]

manufacturer_keys = [
    'form',
    'name',
    'nameInEnglish',
    'country',
    'type'
]

variants_keys = [
    'name', 
    'beginDate',
    'expireDate',
    'activity', 
    'completeness'
]

package_keys = [
    'volume',
    'unitType',
    'amountOfUnits',
    'description'
]

instructions_keys = [
    'type',
    'comment',
    'fileInRussian',
    'fileInKazakh'
]

certificate_keys = [
    'name',
    'type',
    'dates',
    'organ'
]

attributes_keys = [
    'GMP',
    'Генерик',
    'Рецепт',
    'Контроль',
    'Торг. марка',
    'Патент'
]