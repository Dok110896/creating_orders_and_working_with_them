from auth import *
from datetime import datetime
import time
import requests


pnq_list = []
sale_list = []
sale_nom_list = []
menu_list = []
sale_table = []


# Получение списка номенклатур из прайса для формирования разных заказов
def get_price_list():
    current_date = datetime.now().date()
    response = requests.post(standEndpoint, headers=header, json={
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "FastMenu.List",
        "params": {
            "Фильтр": {
                "d": [
                    Company, ColumnCount, Company, str(current_date),
                    "tile",
                    PriceList,
                    RowCount,
                    [],
                    Warehouse
                ],
                "s": [
                    {
                        "t": "Число целое",
                        "n": "BalanceForOrganization"
                    },
                    {
                        "t": "Число целое",
                        "n": "ColumnCount"
                    },
                    {
                        "t": "Число целое",
                        "n": "Company"
                    },
                    {
                        "t": "Строка",
                        "n": "DateTime"
                    },
                    {
                        "t": "Строка",
                        "n": "Mode"
                    },
                    {
                        "t": "Число целое",
                        "n": "PriceList"
                    },
                    {
                        "t": "Число целое",
                        "n": "RowCount"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Строка"
                        },
                        "n": "UUIDsExclude"
                    },
                    {
                        "t": "Число целое",
                        "n": "Warehouse"
                    }
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": None,
            "Навигация": {
                "d": [
                    True,
                    999,
                    0
                ],
                "s": [
                    {
                        "t": "Логическое",
                        "n": "ЕстьЕще"
                    },
                    {
                        "t": "Число целое",
                        "n": "РазмерСтраницы"
                    },
                    {
                        "t": "Число целое",
                        "n": "Страница"
                    }
                ],
                "_type": "record",
                "f": 0
            },
            "ДопПоля": [
                "Certificates"
            ]
        },
        "id": 1
    }).json()
    sale = response['result']['d']
    for row in sale:
        if row[8] is not None:
            menu_list.append(row[8])


def sale_list_table(table):
    response = requests.post(standEndpoint, headers=header, json={
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Sale.RestoreMemo",
        "params": {
            "Params": {
                "d": [
                    None,
                    table,
                    True,
                    None,
                    False,
                    False,
                    True,
                    True
                ],
                "s": [
                    {
                        "t": "Число целое",
                        "n": "Workplace"
                    },
                    {
                        "t": "Число целое",
                        "n": "Location"
                    },
                    {
                        "t": "Логическое",
                        "n": "ShowDiscounts"
                    },
                    {
                        "t": "Число целое",
                        "n": "PriceList"
                    },
                    {
                        "t": "Логическое",
                        "n": "ReversePositions"
                    },
                    {
                        "t": "Логическое",
                        "n": "CreateSale"
                    },
                    {
                        "t": "Логическое",
                        "n": "ShowGuests"
                    },
                    {
                        "t": "Логическое",
                        "n": "ShowTables"
                    }
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }).json()

    sale = response['result']['d']
    for row in sale:
        sale_table.append(row[0])


def delete_order_table():
    start_time = time.time()
    for d in range(len(sale_table)):
        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "Sale.Cancel",
            "params": {
                "Sale": sale_table[d],
                "RefusalReason": 5,
                "Workplace": None,
                "AuthInfo": None,
                "Params": {
                    "d": [
                        True
                    ],
                    "s": [
                        {
                            "t": "Логическое",
                            "n": "CheckUnfinishedTasks"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        }).json()

        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "Sale.Cancel",
            "params": {
                "Sale": sale_table[d],
                "RefusalReason": None,
                "Workplace": None,
                "AuthInfo": None,
                "Params": {
                    "d": [
                        True
                    ],
                    "s": [
                        {
                            "t": "Логическое",
                            "n": "CheckUnfinishedTasks"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        }).json()
    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Все заказы удалены за {elapsed_time} сек.\n")


def delete_tables():
    number = int(input("Введите номер столика для удаления заказов: \n"))
    table = table_num[number]
    sale_list_table(table)
    if sale_table != []:
        delete_order_table()
    else:
        print("На этом столике больше нет активных заказов")
