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


# Подключение к БД PostgreSQL
CONNECTION, CURSOR = connect_to_database()

# Открытие документа Google Sheets
sa = gspread.service_account(filename="creds.json")
sh = sa.open("Copy of test")

# Чтение данных из документа
worksheet = sh.worksheet("Лист1")
order_data = worksheet.get_all_values()
print('list_of_lists:', order_data)
