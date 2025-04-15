from datetime import datetime, time

from auth import *
from order_actions import delete_tables
from user_settings import *

pnq_list = []


async def async_post(client, json_data):
    try:
        response = await client.post(standEndpoint, json=json_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request error: {str(e)}")
        return None


async def set_pnq_state(state):
    # start_time = time.time()
    async with httpx.AsyncClient(headers=header) as client:
        tasks = []
        for pnq in pnq_list:
            data = {
                "jsonrpc": "2.0",
                "protocol": 6,
                "method": "ProductionNomenclatureQueue.SetState",
                "params": {
                    "Param": {
                        "d": [[Company], [pnq], state],
                        "s": [
                            {"t": {"n": "Массив", "t": "Число целое"}, "n": "Companies"},
                            {"t": {"n": "Массив", "t": "Число целое"}, "n": "ProductionNomenclatureQueues"},
                            {"t": "Число целое", "n": "State"}
                        ],
                        "_type": "record",
                        "f": 0
                    }
                },
                "id": 1
            }
            tasks.append(async_post(client, data))

        await asyncio.gather(*tasks)

    # end_time = time.time()
    # elapsed_time = round((end_time - start_time), 2)
    state_name = {
        10: "готовыми",
        15: "поданы",
        5: "в работу"
    }.get(state, "")
    # print(f"Все заказы отмечены {state_name} за {elapsed_time} сек.")
    print(f"Все заказы отмечены {state_name} ")


async def check_ready():
    await set_pnq_state(10)


async def check_served():
    await set_pnq_state(15)
    await verify_empty_kitchen()


async def check_in_work():
    await set_pnq_state(5)


async def verify_empty_kitchen():
    current_date = datetime.now().date()
    data = {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Kitchen.TaskList",
        "params": {
            "Фильтр": {
                "d": [False, Company, True, "in_work",
                      [str(current_date), str(current_date)],
                      [None], None, True, [0, 5, 10], [Warehouse]],
                "s": [
                    {"t": "Логическое", "n": "ByNomenclature"},
                    {"t": "Число целое", "n": "Company"},
                    {"t": "Логическое", "n": "IsOnline"},
                    {"t": "Строка", "n": "Mode"},
                    {"t": {"n": "Массив", "t": "Дата"}, "n": "Period"},
                    {"t": {"n": "Массив", "t": "Строка"}, "n": "ProductionSites"},
                    {"t": "Строка", "n": "Search"},
                    {"t": "Логическое", "n": "ShowDelivery"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "States"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "Warehouses"}
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": {"d": [[False, "Started", True]]},
            "Навигация": {"d": [True, 999, 0]},
            "ДопПоля": []
        },
        "id": 1
    }

    async with httpx.AsyncClient(headers=header) as client:
        response = await async_post(client, data)
        if response:
            av = [row[16] for row in response['result']['d']]
            assert len(av) == 0, "На кухне остались блюда"


async def get_pnq_list():
    current_date = "2025-04-15"  # Фиксированная дата для тестирования
    # data = {
    #     "jsonrpc": "2.0",
    #     "protocol": 6,
    #     "method": "Kitchen.TaskList",
    #     "params": {
    #         "Фильтр": {
    #             "d": [False, Company, True, "in_work",
    #                   [current_date, current_date],
    #                   [None], None, True, [0, 5, 10], [Warehouse]],
    #             "s": [
    #                 {"t": "Логическое", "n": "ByNomenclature"},
    #                 {"t": "Число целое", "n": "Company"},
    #                 {"t": "Логическое", "n": "IsOnline"},
    #                 {"t": "Строка", "n": "Mode"},
    #                 {"t": {"n": "Массив", "t": "Дата"}, "n": "Period"},
    #                 {"t": {"n": "Массив", "t": "Строка"}, "n": "ProductionSites"},
    #                 {"t": "Строка", "n": "Search"},
    #                 {"t": "Логическое", "n": "ShowDelivery"},
    #                 {"t": {"n": "Массив", "t": "Число целое"}, "n": "States"},
    #                 {"t": {"n": "Массив", "t": "Число целое"}, "n": "Warehouses"}
    #             ],
    #             "_type": "record",
    #             "f": 0
    #         },
    #         "Сортировка": {"d": [[False, "Started", True]]},
    #         "Навигация": {"d": [True, 999, 0]},
    #         "ДопПоля": []
    #     },
    #     "id": 1
    # }
    data = {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "Kitchen.TaskList",
        "params": {
            "Фильтр": {
                "d": [True, 3395, True, "ready", ["2025-04-15", "2025-04-15"], [None], True, [15], [3397]],
                "s": [
                    {"t": "Логическое", "n": "ByNomenclature"},
                    {"t": "Число целое", "n": "Company"},
                    {"t": "Логическое", "n": "IsOnline"},
                    {"t": "Строка", "n": "Mode"},
                    {"t": {"n": "Массив", "t": "Дата"}, "n": "Period"},
                    {"t": {"n": "Массив", "t": "Строка"}, "n": "ProductionSites"},
                    {"t": "Логическое", "n": "ShowDelivery"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "States"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "Warehouses"}
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": {
                "d": [[False, "Started", True]],
                "s": [
                    {"t": "Логическое", "n": "l"},
                    {"t": "Строка", "n": "n"},
                    {"t": "Логическое", "n": "o"}
                ],
                "_type": "recordset",
                "f": 0
            },
            "Навигация": {
                "d": ["forward", True, 999, None],
                "s": [
                    {"t": "Строка", "n": "Direction"},
                    {"t": "Логическое", "n": "HasMore"},
                    {"t": "Число целое", "n": "Limit"},
                    {"t": "Строка", "n": "Position"}
                ],
                "_type": "record",
                "f": 0
            },
            "ДопПоля": []
        },
        "id": 1
    }

    async with httpx.AsyncClient(headers=header) as client:
        try:
            response = await async_post(client, data)

            # Включите для отладки, чтобы видеть полный ответ:
            # print("Полный ответ от сервера:", response)

            if not response:
                print("Пустой ответ от сервера")
                return []

            if 'error' in response:
                print(f"Ошибка API: {response['error']}")
                return []

            if 'result' not in response:
                print("Ответ не содержит ключа 'result'")
                return []

            # result_data = response['result']

            # if 'd' not in result_data:
            #     print("Ответ не содержит данных в 'd'")
            #     return []

            # Обрабатываем данные
            global pnq_list
            pnq_list = []

            for row in response['result']['d']:
                try:
                    if len(row) > 18:
                        pnq_list.append(row[18])
                    else:
                        print(f"Пропуск строки - недостаточно элементов ({len(row)} из 19)")
                except Exception as e:
                    print(f"Ошибка обработки строки: {str(e)}")

            if not pnq_list:
                print("Нет активных заказов (pnq_list пуст)")

            return pnq_list

        except Exception as e:
            print(f"Ошибка в get_pnq_list: {str(e)}")
            return []


async def pnq_actions():
    await get_pnq_list()

    if not pnq_list:
        print("Нет активных заказов")
        return

    action = int(input(
        "\nВыберите действие над заказами:\n"
        "1. Отметить всё готовым\n"
        "2. Отметить всё выданным\n"
        "3. Вернуть всё в работу\n"
        "4. Удалить заказы на столике\n"
        "Ваш выбор: "))

    if action == 1:
        await check_ready()
        answer = int(input("\nОтметить все блюда выданными:\n1 - Да,\n2 - Нет\nВаш ответ: "))
        if answer == 1:
            await get_pnq_list()
            await check_served()
    elif action == 2:
        await check_served()
    elif action == 3:
        await check_in_work()
        print('Все блюда возвращены в работу')
    elif action == 4:
        await delete_tables()