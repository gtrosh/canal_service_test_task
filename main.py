import datetime
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import apiclient.discovery
import gspread
import httplib2
import psycopg2
from oauth2client.service_account import ServiceAccountCredentials
from psycopg2 import extras


def connect_to_database():
    '''Осуществляет подключение к базе данных'''
    connection = psycopg2.connect(dbname='canal_service', user='postgres',
                                  password='Potter2021&', host='localhost', port='5432')
    cursor = connection.cursor()
    return connection, cursor


def get_exchange_rate(url):
    '''Возвращает стоимость одного доллара США в рублях по курсу ЦБ РФ'''
    html = urllib.request.urlopen(link).read().decode(encoding="windows-1251")
    data = ET.fromstring(html)
    usd_exchange_rate = float(
        (data.find("Valute[@ID='R01235']/Value").text).replace(',', '.'))
    return usd_exchange_rate


def get_order_numbers(CONNECTION, CURSOR):
    '''Получает список номеров заказов, которые на данный момент находятся в базе данных PostgreSQL'''
    check_query = '''select "заказ №" from orders;'''
    CURSOR.execute(check_query)
    order_numbers = CURSOR.fetchall()
    numbers = [number[0] for number in order_numbers]
    return numbers


def delete_orders(CONNECTION, CURSOR, orders):
    '''Удаляет записи о заказах, которых более нет в исходном файле Google Sheets'''
    delete_query = f'''delete from orders where "заказ №" in {orders}'''
    CURSOR.execute(delete_query)
    CONNECTION.commit()


# Открытие документа Google Sheets
sa = gspread.service_account(filename="creds.json")
sh = sa.open("Copy of test")

# Чтение данных из документа Google Sheets
worksheet = sh.worksheet("Лист1")
order_data = worksheet.get_all_values()

# Подключение к БД PostgreSQL
CONNECTION, CURSOR = connect_to_database()

# Проверка данных, содержащихся в БД PostgreSQL
database_orders = get_order_numbers(CONNECTION, CURSOR)
current_orders = [int(order[1]) for order in order_data[1:]]
obsolete_orders = tuple()
for order in database_orders:
    if order not in current_orders:
        obsolete_orders += (order,)

# Удаление неактуальных заказов, которых уже нет в документе Google Sheets
if obsolete_orders:
    delete_orders(CONNECTION, CURSOR, obsolete_orders)

# Получение текущего курса доллара США
link = 'https://www.cbr.ru/scripts/XML_daily.asp'
exchange_rate = get_exchange_rate(link)

# Форматирование полученных данных перед добавлением в таблицу
for order in order_data[1:]:
    for i in range(3):
        order[i] = int(order[i])
    order[3] = datetime.datetime.strptime(order[3], "%d.%m.%Y").date()
    ruble_price = order[2] * exchange_rate
    order += [int(ruble_price)]

# Обработка информации, которую необходимо записать в базу данных PostgreSQL
orders = [tuple(order) for order in order_data[1:]]

args = ','.join(CURSOR.mogrify("(%s,%s,%s,%s,%s)", i).decode('utf-8')
                for i in orders)

insert_query = "INSERT INTO orders VALUES " + \
    (args) + ' on conflict ("заказ №") do update set "стоимость,$"=excluded."стоимость,$", "срок поставки"=excluded."срок поставки", "стоимость в руб."=excluded."стоимость в руб."'
CURSOR.execute(insert_query)
CONNECTION.commit()
CONNECTION.close()
print("Скрипт успешно завершил работу!")
