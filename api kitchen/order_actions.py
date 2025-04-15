import asyncio
import httpx
from auth import *
from user_settings import *
from datetime import datetime
import time
from tenacity import retry, stop_after_attempt, wait_exponential


MAX_CONCURRENT_DELETES = 90  # Лимит одновременных удалений в одной очереди
DELETE_TIMEOUT = 30.0  # Таймаут для каждого запроса
RETRY_ATTEMPTS = 3  # Количество попыток повтора
QUEUE_DELAY = 2  # Задержка между очередями в секундах


async def async_post(client, json_data):
    try:
        response = await client.post(standEndpoint, json=json_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request error: {str(e)}")
        return None


async def get_price_list():
    current_date = datetime.now().date()
    data = {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "FastMenu.List",
        "params": {
            "Фильтр": {
                "d": [Company, ColumnCount, Company, str(current_date),
                      "tile", PriceList, RowCount, [], Warehouse],
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
            "Навигация": {"d": [True, 999, 0]},
            "ДопПоля": ["Certificates"]
        },
        "id": 1
    }

    async with httpx.AsyncClient(headers=header) as client:
        response = await async_post(client, data)
        if response and 'result' in response:
            return [row[8] for row in response['result']['d'] if row[8] is not None]
    return []


async def sale_list_table(table):
    data = {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Sale.RestoreMemo",
        "params": {
            "Params": {
                "d": [None, table, True, None, False, False, True, True],
                "s": [
                    {"t": "Число целое", "n": "Workplace"},
                    {"t": "Число целое", "n": "Location"},
                    {"t": "Логическое", "n": "ShowDiscounts"},
                    {"t": "Число целое", "n": "PriceList"},
                    {"t": "Логическое", "n": "ReversePositions"},
                    {"t": "Логическое", "n": "CreateSale"},
                    {"t": "Логическое", "n": "ShowGuests"},
                    {"t": "Логическое", "n": "ShowTables"}
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }

    async with httpx.AsyncClient(headers=header) as client:
        response = await async_post(client, data)
        if response and 'result' in response:
            return [row[0] for row in response['result']['d']]
    return []


@retry(
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def delete_order(client: httpx.AsyncClient, sale_id: int, index: int = None) -> None:
    try:
        cancel_data = {
            "jsonrpc": "2.0",
            "protocol": 6,
            "method": "Sale.Cancel",
            "params": {
                "Sale": sale_id,
                "RefusalReason": 5,
                "Workplace": None,
                "AuthInfo": None,
                "Params": {
                    "d": [True],
                    "s": [{"t": "Логическое", "n": "CheckUnfinishedTasks"}],
                    "_type": "record",
                    "f": 0
                }
            },
            "id": 1
        }

        # Отправляем оба варианта запроса (с RefusalReason и без)
        responses = await asyncio.gather(
            client.post(standEndpoint, json=cancel_data, headers=header, timeout=DELETE_TIMEOUT),
            client.post(standEndpoint,
                        json={**cancel_data, "params": {**cancel_data["params"], "RefusalReason": None}},
                        headers=header,
                        timeout=DELETE_TIMEOUT)
        )

        for response in responses:
            response.raise_for_status()

        if index is not None:
            print(f"Заказ {index + 1} (ID: {sale_id}) успешно удален")
    except Exception as e:
        print(f"Ошибка при удалении заказа {f'{index + 1} ' if index is not None else ''}(ID: {sale_id}): {str(e)}")
        raise


async def delete_order_table(sale_ids: list) -> None:
    start_time = time.time()

    # Создаем клиент с настройками пула соединений
    async with httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=MAX_CONCURRENT_DELETES,
                max_keepalive_connections=50,
                keepalive_expiry=60
            ),
            timeout=httpx.Timeout(DELETE_TIMEOUT)
    ) as client:
        # Разбиваем все заказы на очереди
        total_queues = (len(sale_ids) + MAX_CONCURRENT_DELETES - 1) // MAX_CONCURRENT_DELETES

        for queue_num in range(total_queues):
            start_index = queue_num * MAX_CONCURRENT_DELETES
            end_index = min((queue_num + 1) * MAX_CONCURRENT_DELETES, len(sale_ids))
            current_batch = sale_ids[start_index:end_index]

            print(f"\nОбработка очереди {queue_num + 1}/{total_queues} "
                  f"(заказы {start_index + 1}-{end_index})")

            # Создаем задачи для текущей очереди
            tasks = [
                delete_order(client, sale_id, start_index + i)
                for i, sale_id in enumerate(current_batch)
            ]

            await asyncio.gather(*tasks)

            # Добавляем задержку между очередями, кроме последней
            if queue_num < total_queues - 1:
                print(f"\nПауза {QUEUE_DELAY} сек. перед следующей очередью...")
                await asyncio.sleep(QUEUE_DELAY)

    elapsed_time = round((time.time() - start_time), 2)
    print(f"\nВсе {len(sale_ids)} заказов удалены за {elapsed_time} сек.")


async def delete_tables():
    number = int(input("Введите номер столика для удаления заказов: \n"))
    table = table_num[number]
    sales = await sale_list_table(table)

    if not sales:
        print("На этом столике нет активных заказов для удаления")
        return

    print(f"\nНайдено {len(sales)} заказов для удаления со столика {number}")
    confirm = input("Вы уверены, что хотите удалить все эти заказы? (y/n): ").lower()

    if confirm == 'y':
        await delete_order_table(sales)
    else:
        print("Удаление отменено")
