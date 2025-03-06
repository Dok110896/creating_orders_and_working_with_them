from kitchen_actions import *
import requests
import uuid
import time


# Пользовательская дата для работы с другими периодами при отметке
user_date = "2024-12-10"

# Переменные внутри методов
sale_list = []
sale_nom_list = []
menu_list = []
sale_table = []


def select():
    ans = int(input(
        "\nЧто нужно сделать?\n"
        "1. Создать заказы\n"
        "2. Работать с заказами\n"
        "Ваш выбор: "))

    if ans == 1:
        print(f"\nУ вас на схеме {len(table_num) - 1} столика")
        number = int(input("Введите номер столика где будут созданы заказы: "))
        table = table_num[number]
        generate_order_send_kitchen(table)

    elif ans == 2:
        return pnq_actions()

    else:
        print("неправильно")


def pnq_actions():
    get_pnq_list()

    action = int(input((
        "\nВыберите действие над заказами:\n"
        "1. Отметить всё готовым\n"
        "2. Отметить всё выданным\n"
        "3. Вернуть всё в работу\n"
        "4. Удалить заказы на столике\n"
        "Ваш выбор: ")))

    if len(pnq_list) != 0:

        # Отметка всех блюд готовыми
        if action == 1:
            check_ready()
            answer = int(input("\nОтметить все блюда выданными:\n"
                               " 1 - Да,\n"
                               " 2 - Нет\n"
                               "Ваш ответ: "))

            if answer == 1:
                get_pnq_list()
                check_served()

            elif answer == 2:
                print("Запустите метод еще раз чтобы выполнить другое действие")

        # Отметка всех блюд выданными
        elif action == 2:
            check_served()

        # Возврат в работу
        elif action == 3:
            check_in_work()
            print('Все блюда возвращены в работу')

    if action == 4:
        print(f"\nУ вас {len(table_num) - 1} столика")
        delete_tables()
        ans = str(input("Удалить заказы за другим столиком? (Да / Нет)\n"
                        "Ваш ответ: "))

        while ans == "Да" or ans == "да":
            delete_tables()
            ans = str(input("Удалить заказы за другим столиком? (Да / Нет)\n"
                            "Ваш ответ: "))


def generate_order_send_kitchen(table):
    count = int(input("\nУкажите количество заказов: "))
    get_price_list()

    start_time = time.time()

    for i in range(count):
        response_sale = requests.post(standEndpoint, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "Sale.Create",
            "params": {
                "Params": {
                    "d": [
                        Company,
                        PriceList,
                        0,
                        {
                            "workplace": workplace,
                            "product": product
                        },
                        "order",
                        table,
                        Seller,
                        True
                    ],
                    "s": [
                        {
                            "t": "Число целое",
                            "n": "Company"
                        },
                        {
                            "t": "Число целое",
                            "n": "PriceList"
                        },
                        {
                            "t": "Число целое",
                            "n": "Type"
                        },
                        {
                            "t": "JSON-объект",
                            "n": "Properties"
                        },
                        {
                            "t": "Строка",
                            "n": "Reglament"
                        },
                        {
                            "t": "Число целое",
                            "n": "Location"
                        },
                        {
                            "t": "Число целое",
                            "n": "Seller"
                        },
                        {
                            "t": "Логическое",
                            "n": "ReturnSellerInfo"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        }, headers=header).json()

        sale = response_sale['result']['d'][0]
        sale_list.append(sale)

        response_add = requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "SaleNomenclature.AddBatch",
            "params": {
                "Options": {
                    "skip_sale_check": True,
                    "pay_type": 0,
                    "skip_calories": True
                },
                "Sale": sale_list[i],
                "Batch": {
                    "d": [
                        [
                            str(uuid.uuid4()),
                            None,
                            None,
                            # menu_list[i],   # список номенклатур
                            # random.choice(menu_list),   # список номенклатур
                            Nomenclature,
                            None,
                            CatalogPrice,
                            Quantity,
                            {
                                "type_ticket": None,
                                "origin_quantity": 1,
                                "skip_serial": None
                            }
                        ]
                    ],
                    "s": [
                        {"t": "UUID", "n": "RecordKey"},
                        {"t": "UUID", "n": "FolderKey"},
                        {"t": "UUID", "n": "Key"},
                        {"t": "Число целое", "n": "Nomenclature"},
                        {"t": "Деньги", "n": "ManualPrice"},
                        {"t": "Деньги", "n": "CatalogPrice"},
                        {"t": "Число вещественное", "n": "Quantity"},
                        {"t": "JSON-объект", "n": "Properties"}
                    ],
                    "_type": "recordset",
                    "f": 0
                }
            },
            "id": 1
        }).json()

        sale_order = response_add["result"]["d"][0][1]
        sale_nom_list.append(sale_order)

        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "Kitchen.SetState",
            "params": {
                "rec": {
                    "d": [
                        5,
                        Warehouse,
                        {
                            "d": [
                                [
                                    sale_nom_list[i],
                                    None,
                                    None,
                                    sale_list[i],
                                    0
                                ]
                            ],
                            "s": [
                                {
                                    "t": "Число целое",
                                    "n": "SaleNomenclature"
                                },
                                {
                                    "t": "Число целое",
                                    "n": "ProductionNomenclatureQueue"
                                },
                                {
                                    "t": "Число целое",
                                    "n": "State"
                                },
                                {
                                    "t": "Число целое",
                                    "n": "Sale"
                                },
                                {
                                    "t": "Число целое",
                                    "n": "Priority"
                                }
                            ],
                            "_type": "recordset",
                            "f": 1
                        },
                        Company,
                        table
                    ],
                    "s": [
                        {
                            "t": "Число целое",
                            "n": "State"
                        },
                        {
                            "t": "Число целое",
                            "n": "Warehouse"
                        },
                        {
                            "t": "Выборка",
                            "n": "SaleNomenclatures"
                        },
                        {
                            "t": "Число целое",
                            "n": "Company"
                        },
                        {
                            "t": "Число целое",
                            "n": "Location"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        })

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"{count} заказ(ов) созданы и отправлены на кухню за {elapsed_time} сек.")
    answer = int(input("\n1. Продолжить работу\n"
                       "2. Закончить\n"
                       "Ваш выбор: "))

    if answer == 1:
        return select()

    elif answer == 2:
        print("Работа метода завершена")


select()
