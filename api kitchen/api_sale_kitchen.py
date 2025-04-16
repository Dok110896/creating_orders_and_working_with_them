from kitchen_actions import *
import httpx
import asyncio
import uuid
import time
from typing import List, Dict, Any
from order_actions import get_price_list
from tenacity import retry, stop_after_attempt, wait_exponential

# Константы для ограничений
MAX_CONCURRENT_REQUESTS = 50  # Лимит одновременных запросов в одной очереди
REQUEST_TIMEOUT = 30.0  # Таймаут для каждого запроса
RETRY_ATTEMPTS = 3  # Количество попыток повтора
QUEUE_DELAY = 1  # Задержка между очередями в секундах


# Пользовательская дата для работы с другими периодами при отметке
user_date = "2024-12-10"

# Переменные внутри методов
sale_list: List[int] = []
sale_nom_list: List[int] = []
menu_list: List[int] = []
sale_table: List[int] = []


async def select() -> None:
    ans = int(input(
        "\nЧто нужно сделать?\n"
        "1. Создать заказы\n"
        "2. Работать с заказами\n"
        "Ваш выбор: "))

    if ans == 1:
        print(f"\nУ вас на схеме {len(table_num) - 1} столика")
        number = int(input("Введите номер столика где будут созданы заказы: "))
        table = table_num[number]
        await generate_order_send_kitchen(table)

    elif ans == 2:
        await pnq_actions()
    else:
        print("Неправильный выбор")


async def pnq_actions() -> None:
    await get_pnq_list()

    action = int(input((
        "\nВыберите действие над заказами:\n"
        "1. Отметить всё готовым\n"
        "2. Отметить всё выданным\n"
        "3. Вернуть всё в работу\n"
        "4. Удалить заказы на столике\n"
        "Ваш выбор: ")))

    if len(pnq_list) != 0:
        if action == 1:
            await check_ready()
            answer = int(input("\nОтметить все блюда выданными:\n"
                               "1 - Да,\n"
                               "2 - Нет\n"
                               "Ваш ответ: "))

            if answer == 1:
                await get_pnq_list()
                await check_served()
            elif answer == 2:
                print("Запустите метод еще раз чтобы выполнить другое действие")

        elif action == 2:
            await check_served()

        elif action == 3:
            await check_in_work()
            print('Все блюда возвращены в работу')

    if action == 4:
        print(f"\nУ вас {len(table_num) - 1} столика")
        await delete_tables()


@retry(
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def create_and_send_order(client: httpx.AsyncClient, table: int, index: int) -> None:
    try:
        # Создание продажи
        sale_response = await client.post(
            standEndpoint,
            json={
                "jsonrpc": "2.0",
                "protocol": 6,
                "method": "Sale.Create",
                "params": {
                    "Params": {
                        "d": [
                            Company,
                            PriceList,
                            0,
                            {"workplace": workplace, "product": product},
                            "order",
                            table,
                            Seller,
                            True
                        ],
                        "s": [
                            {"t": "Число целое", "n": "Company"},
                            {"t": "Число целое", "n": "PriceList"},
                            {"t": "Число целое", "n": "Type"},
                            {"t": "JSON-объект", "n": "Properties"},
                            {"t": "Строка", "n": "Reglament"},
                            {"t": "Число целое", "n": "Location"},
                            {"t": "Число целое", "n": "Seller"},
                            {"t": "Логическое", "n": "ReturnSellerInfo"}
                        ],
                        "_type": "record",
                        "f": 0
                    }
                },
                "id": 1
            },
            headers=header,
            timeout=REQUEST_TIMEOUT
        )
        sale_response.raise_for_status()
        sale_data = sale_response.json()
        sale = sale_data['result']['d'][0]

        # Добавление номенклатуры
        add_response = await client.post(
            standEndpoint,
            headers=header,
            json={
                "jsonrpc": "2.0",
                "protocol": 6,
                "method": "SaleNomenclature.AddBatch",
                "params": {
                    "Options": {
                        "skip_sale_check": True,
                        "pay_type": 0,
                        "skip_calories": True
                    },
                    "Sale": sale,
                    "Batch": {
                        "d": [
                            [
                                str(uuid.uuid4()),
                                None,
                                None,
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
            },
            timeout=REQUEST_TIMEOUT
        )
        add_response.raise_for_status()
        add_data = add_response.json()
        sale_order = add_data["result"]["d"][0][1]

        # Отправка на кухню
        await client.post(
            standEndpoint,
            headers=header,
            json={
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
                                        sale_order,
                                        None,
                                        None,
                                        sale,
                                        0
                                    ]
                                ],
                                "s": [
                                    {"t": "Число целое", "n": "SaleNomenclature"},
                                    {"t": "Число целое", "n": "ProductionNomenclatureQueue"},
                                    {"t": "Число целое", "n": "State"},
                                    {"t": "Число целое", "n": "Sale"},
                                    {"t": "Число целое", "n": "Priority"}
                                ],
                                "_type": "recordset",
                                "f": 1
                            },
                            Company,
                            table
                        ],
                        "s": [
                            {"t": "Число целое", "n": "State"},
                            {"t": "Число целое", "n": "Warehouse"},
                            {"t": "Выборка", "n": "SaleNomenclatures"},
                            {"t": "Число целое", "n": "Company"},
                            {"t": "Число целое", "n": "Location"}
                        ],
                        "_type": "record",
                        "f": 0
                    }
                },
                "id": 1
            },
            timeout=REQUEST_TIMEOUT
        )
        print(f"Заказ {index + 1} успешно обработан")
    except Exception as e:
        print(f"Ошибка при обработке заказа {index + 1}: {str(e)}")
        raise


async def generate_order_send_kitchen(table: int) -> None:
    count = int(input("\nУкажите количество заказов: "))
    await get_price_list()

    start_time = time.time()

    # Создаем клиент с настройками пула соединений
    async with httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=MAX_CONCURRENT_REQUESTS,
                max_keepalive_connections=50,
                keepalive_expiry=60
            ),
            timeout=httpx.Timeout(REQUEST_TIMEOUT)
    ) as client:
        # Разбиваем все заказы на очереди по 100
        total_queues = (count + MAX_CONCURRENT_REQUESTS - 1) // MAX_CONCURRENT_REQUESTS

        for queue_num in range(total_queues):
            start_index = queue_num * MAX_CONCURRENT_REQUESTS
            end_index = min((queue_num + 1) * MAX_CONCURRENT_REQUESTS, count)

            print(f"\nОбработка очереди {queue_num + 1}/{total_queues} "
                  f"(заказы {start_index + 1}-{end_index})")

            # Создаем задачи для текущей очереди
            tasks = [
                create_and_send_order(client, table, i)
                for i in range(start_index, end_index)
            ]

            await asyncio.gather(*tasks)

            # Добавляем задержку между очередями, кроме последней
            if queue_num < total_queues - 1:
                print(f"\nПауза {QUEUE_DELAY} сек. перед следующей очередью...")
                await asyncio.sleep(QUEUE_DELAY)

    elapsed_time = round((time.time() - start_time), 2)
    print(f"\nВсе {count} заказов созданы и отправлены на кухню за {elapsed_time} сек.")

    answer = int(input("\n1. Продолжить работу\n"
                       "2. Закончить\n"
                       "Ваш выбор: "))

    if answer == 1:
        await select()
    elif answer == 2:
        print("Работа метода завершена")


async def main():
    await select()


if __name__ == "__main__":
    asyncio.run(main())
