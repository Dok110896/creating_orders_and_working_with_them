import uuid
import schedule
import time
from auth import *
from datetime import datetime, time as dt_time

# Конфигурация
WORK_START = dt_time(8, 0)  # Начало рабочего времени
WORK_END = dt_time(19, 0)  # Конец рабочего времени
INTERVAL_MINUTES = 7  # Интервал между заказами
ORDERS_PER_BATCH = 10  # Количество заказов за один раз

# Инициализация списков
menu_list = []
sale_list = []
sale_nom_list = []
table = 4605


def get_price_list():
    """Получение списка товаров из API"""
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
                    {"t": "Число целое", "n": "BalanceForOrganization"},
                    {"t": "Число целое", "n": "ColumnCount"},
                    {"t": "Число целое", "n": "Company"},
                    {"t": "Строка", "n": "DateTime"},
                    {"t": "Строка", "n": "Mode"},
                    {"t": "Число целое", "n": "PriceList"},
                    {"t": "Число целое", "n": "RowCount"},
                    {"t": {"n": "Массив", "t": "Строка"}, "n": "UUIDsExclude"},
                    {"t": "Число целое", "n": "Warehouse"}
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": None,
            "Навигация": {
                "d": [True, 999, 0],
                "s": [
                    {"t": "Логическое", "n": "ЕстьЕще"},
                    {"t": "Число целое", "n": "РазмерСтраницы"},
                    {"t": "Число целое", "n": "Страница"}
                ],
                "_type": "record",
                "f": 0
            },
            "ДопПоля": ["Certificates"]
        },
        "id": 1
    }).json()

    menu_list.clear()  # Очищаем список перед заполнением
    for row in response['result']['d']:
        if row[8] is not None:
            menu_list.append(row[8])


def generate_orders():
    """Генерация партии заказов"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Начало формирования {ORDERS_PER_BATCH} заказов")

    get_price_list()

    if not menu_list:
        print("Ошибка: список товаров пуст!")
        return

    successful_orders = 0
    for i in range(ORDERS_PER_BATCH):
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

        successful_orders += 1

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Успешно создано {successful_orders}/{ORDERS_PER_BATCH} заказов")


def job():
    """Проверка времени и запуск генерации заказов"""
    now = datetime.now().time()

    if WORK_START <= now <= WORK_END:
        generate_orders()
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] Сейчас не рабочее время ({WORK_START.strftime('%H:%M')}-{WORK_END.strftime('%H:%M')})")


def run_scheduler():
    """Запуск планировщика"""
    # Первый запуск сразу при старте (если рабочее время)
    auth_fix()
    job()
    # Затем по расписанию
    schedule.every(INTERVAL_MINUTES).minutes.do(job)

    print("Планировщик запущен. Формирование заказов по расписанию...")
    print(f"Текущее время: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Рабочий интервал: {WORK_START.strftime('%H:%M')}-{WORK_END.strftime('%H:%M')}, каждые {INTERVAL_MINUTES} минут")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\nПланировщик остановлен")