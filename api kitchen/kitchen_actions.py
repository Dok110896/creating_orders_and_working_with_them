from order_actions import *
from auth import *
import requests
import time
from datetime import datetime


pnq_list = []


def check_ready():
    i = 0
    start_time = time.time()
    while i < len(pnq_list):
        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "ProductionNomenclatureQueue.SetState",
            "params": {
                "Param": {
                    "d": [
                        [
                            Company
                        ],
                        [
                            pnq_list[i]
                        ],
                        10
                    ],
                    "s": [
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "Companies"
                        },
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "ProductionNomenclatureQueues"
                        },
                        {
                            "t": "Число целое",
                            "n": "State"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        })
        i += 1
        # time.sleep(0.1)
    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Все заказы отмечены готовыми за {elapsed_time} сек.")


# Отметка выдано
def check_served():
    i = 0
    start_time = time.time()
    while i < len(pnq_list):
        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "ProductionNomenclatureQueue.SetState",
            "params": {
                "Param": {
                    "d": [
                        [
                            Company
                        ],
                        [
                            pnq_list[i]
                        ],
                        15
                    ],
                    "s": [
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "Companies"
                        },
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "ProductionNomenclatureQueues"
                        },
                        {
                            "t": "Число целое",
                            "n": "State"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1})
        i += 1
        # time.sleep(0.1)

    av = []
    current_date = datetime.now().date()
    response = requests.post(standEndpoint, headers=header, json={
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Kitchen.TaskList",
        "params": {
            "Фильтр": {
                "d": [
                    False,
                    Company,
                    True,
                    "in_work",
                    [
                        # user_date,
                        # user_date,
                        str(current_date),
                        str(current_date)
                    ],
                    [
                        None
                    ],
                    None,
                    True,
                    [
                        0,
                        5,
                        10
                    ],
                    [
                        Warehouse
                    ]
                ],
                "s": [
                    {
                        "t": "Логическое",
                        "n": "ByNomenclature"
                    },
                    {
                        "t": "Число целое",
                        "n": "Company"
                    },
                    {
                        "t": "Логическое",
                        "n": "IsOnline"
                    },
                    {
                        "t": "Строка",
                        "n": "Mode"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Дата"
                        },
                        "n": "Period"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Строка"
                        },
                        "n": "ProductionSites"
                    },
                    {
                        "t": "Строка",
                        "n": "Search"
                    },
                    {
                        "t": "Логическое",
                        "n": "ShowDelivery"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Число целое"
                        },
                        "n": "States"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Число целое"
                        },
                        "n": "Warehouses"
                    }
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": {
                "d": [
                    [
                        False,
                        "Started",
                        True
                    ]
                ],
                "s": [
                    {
                        "t": "Логическое",
                        "n": "l"
                    },
                    {
                        "t": "Строка",
                        "n": "n"
                    },
                    {
                        "t": "Логическое",
                        "n": "o"
                    }
                ],
                "_type": "recordset",
                "f": 0
            },
            "Навигация": {
                "d": [
                    True,
                    999,  # по умолчанию 30 записей
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
            "ДопПоля": []
        },
        "id": 1
    }).json()
    sale = response['result']['d']
    for row in sale:
        av.append(row[16])

    assert len(av) == 0, "На кухне остались блюда"
    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Все заказы отмечены поданы за {elapsed_time} сек.")


# вернуть в работу
def check_in_work():
    i = 0
    start_time = time.time()
    while i < len(pnq_list):
        requests.post(standEndpoint, headers=header, json={
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "ProductionNomenclatureQueue.SetState",
            "params": {
                "Param": {
                    "d": [
                        [
                            Company
                        ],
                        [
                            pnq_list[i]
                        ],
                        5
                    ],
                    "s": [
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "Companies"
                        },
                        {
                            "t": {
                                "n": "Массив",
                                "t": "Число целое"
                            },
                            "n": "ProductionNomenclatureQueues"
                        },
                        {
                            "t": "Число целое",
                            "n": "State"
                        }
                    ],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1})
        i += 1
    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print(f"Все заказы отмечены в работу за {elapsed_time} сек.")


# Получение списка блюд на кухне
def get_pnq_list():
    current_date = datetime.now().date()
    response = requests.post(standEndpoint, headers=header, json={
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Kitchen.TaskList",
        "params": {
            "Фильтр": {
                "d": [
                    False,
                    Company,
                    True,
                    "in_work",
                    [
                        # user_date,
                        # user_date,
                        str(current_date),
                        str(current_date)
                    ],
                    [
                        None
                    ],
                    None,
                    True,
                    [
                        0,
                        5,
                        10
                    ],
                    [
                        Warehouse
                    ]
                ],
                "s": [
                    {
                        "t": "Логическое",
                        "n": "ByNomenclature"
                    },
                    {
                        "t": "Число целое",
                        "n": "Company"
                    },
                    {
                        "t": "Логическое",
                        "n": "IsOnline"
                    },
                    {
                        "t": "Строка",
                        "n": "Mode"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Дата"
                        },
                        "n": "Period"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Строка"
                        },
                        "n": "ProductionSites"
                    },
                    {
                        "t": "Строка",
                        "n": "Search"
                    },
                    {
                        "t": "Логическое",
                        "n": "ShowDelivery"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Число целое"
                        },
                        "n": "States"
                    },
                    {
                        "t": {
                            "n": "Массив",
                            "t": "Число целое"
                        },
                        "n": "Warehouses"
                    }
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": {
                "d": [
                    [
                        False,
                        "Started",
                        True
                    ]
                ],
                "s": [
                    {
                        "t": "Логическое",
                        "n": "l"
                    },
                    {
                        "t": "Строка",
                        "n": "n"
                    },
                    {
                        "t": "Логическое",
                        "n": "o"
                    }
                ],
                "_type": "recordset",
                "f": 0
            },
            "Навигация": {
                "d": [
                    True,
                    999,  # по умолчанию 30 записей
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
            "ДопПоля": []
        },
        "id": 1
    }).json()
    sale = response['result']['d']
    for row in sale:
        pnq_list.append(row[17])
