import asyncio
import httpx
from auth import *
from user_settings import *
from datetime import datetime, time


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


async def delete_order(sale_id):
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

    async with httpx.AsyncClient(headers=header) as client:
        await asyncio.gather(
            async_post(client, cancel_data),
            async_post(client, {**cancel_data, "params": {**cancel_data["params"], "RefusalReason": None}})
        )


async def delete_order_table(sale_table):
    start_time = time.time()
    async with httpx.AsyncClient(headers=header) as client:
        tasks = [delete_order(sale_id) for sale_id in sale_table]
        await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Все заказы удалены за {round((end_time - start_time), 2)} сек.\n")


async def delete_tables():
    number = int(input("Введите номер столика для удаления заказов: \n"))
    table = table_num[number]
    sales = await sale_list_table(table)

    if sales:
        await delete_order_table(sales)
    else:
        print("На этом столике больше нет активных заказов")

    ans = input("Удалить заказы за другим столиком? (Да/Нет)\nВаш ответ: ").lower()
    while ans == "да":
        await delete_tables()
        ans = input("Удалить заказы за другим столиком? (Да/Нет)\nВаш ответ: ").lower()