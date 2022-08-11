# Подготовка
## Клонирование репозитория
```bash
# создайте папку для вашего проекта
mkdir <название-вашей-папки>
# перейдите в эту папку:
cd <название-вашей-папки>
# склонируйте этот репозиторий:
git@github.com:gtrosh/google_sheets_to_postgres_downloader.git
```

## Установка зависимостей
Установить необходимые зависимости из requirements.txt
```bash
pip install -r requirements.txt
```

## Подключение к базе данных PostgreSQL
В функции `connect_to_database` изменить настройки для базы данных PostgreSQL на ваши собственные:
```Python
def connect_to_database():
    connection = psycopg2.connect(dbname='<название-базы-данных>', user='<имя-пользователя>',
                                  password='<пароль-базы-данных>', host='<хост>', port='<номер-порта>')
    cursor = connection.cursor()
    return connection, cursor
```

## Настройки сервисной учетной записи Google API
Поместить файл с данными сервисной учетной записи Google API в директорию, где сохранен скрипт. Изменить название файла в атрибуте `filename` на название вашего файла, а в переменной `sh` укажите название вашего документа Google Sheets.
```Python
sa = gspread.service_account(filename="<имя-файла>")
sh = sa.open("<название-документа-Google-Sheets>")
```

## Данные документа Google Sheets
Проверить и при необходимости изменить название листа в документе Google Sheets, которое хранится в переменной worksheet (в русскоязычной версии обычно лист обычно называется "Лист1", например)
```Python
worksheet = sh.worksheet("<название-листа>")
```

##  Запуск скрипта:
В терминале / командной строке запустить скрипт. 
На `Linux`/`Mac OS` ввести команду:
```bash
python3 main.py
```
На `Windows` ввести команду:
```bash
python main.py
```
