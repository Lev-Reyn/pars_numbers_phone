import requests
from typing import Dict, List
from datetime import date
import csv

token = 'b696fcf63d827b681c5d633fd9ec52863364b596ce624a76fdb284f54afffce96b28598c577591c822fd2'


def calculate_age(born: Dict[str, int]) -> int:
    """считает колличество лет по дате"""
    today = date.today()
    return today.year - born['year'] - ((today.month, today.day) < (born['month'], born['day']))


data_list = []


def pars_numbers(id_men):
    """
    сбор номеров телефонов всех друзей id человека, которого мы закинули в id_men
    функция ничего не возвращает, а просто закидывает данные в data_list
    """

    url = f'https://api.vk.com/method/friends.get?user_id={id_men}&fields=domain,sex,bdate,city,country,id,contacts&ord\
er=random&access_token={token}&v=5.52'

    data = requests.get(url).json()
    if 'error' in data:
        if data['error']['error_msg'] == "Access denied: this profile is private":
            print(f'аккаунт https://vk.com/id{id_men} приватный, пропускаем')
        return
    for men in data['response']['items']:
        if 'mobile_phone' in men and len(men['mobile_phone'].replace('+7', '8')) == 11 and \
                men['mobile_phone'].replace('+7', '8').isdigit() == True:
            name = men["first_name"]
            last_name = men['last_name']
            phone = men["mobile_phone"].replace("+7", "8")
            try:
                bdate = men['bdate']
                if len(bdate.split('.')) == 3:
                    bdate = list(map(int, bdate.split('.')))
                    born = {
                        'day': bdate[0],
                        'month': bdate[1],
                        'year': bdate[2]
                    }
                    years = calculate_age(born)
                    bdate = list(map(str, bdate))
                    bdate = ':'.join(bdate)
                else:
                    years = None
            except KeyError:
                years = None
                bdate = None

            data_dict = {
                'name': name,
                'last name': last_name,
                'birthday': bdate,
                'years': years,
                'phone': phone
            }
            data_list.append(data_dict)
            # print(f'{name} {last_name} {bdate} {years} - {phone}')


id_men = '5847911'
url = f'https://api.vk.com/method/friends.get?user_id={id_men}&access_token={token}&v=5.52'
data_id_json = requests.get(url).json()
count = 0

for id_men in data_id_json['response']['items']:
    pars_numbers(id_men)
    count += 1
    print(f"прошли {count} друзей из {len(data_id_json['response']['items'])}")

with open('data.csv', 'w', newline='') as file:
    fieldnames = []
    for elem in data_list[0]:
        fieldnames.append(elem)
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data_dict in data_list:
        writer.writerow(data_dict)
