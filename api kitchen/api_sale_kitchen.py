from kitchen_actions import *
import httpx
import asyncio
import uuid
import time
from typing import List, Dict, Any
from order_actions import get_price_list

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
        ans = str(input("Удалить заказы за другим столиком? (Да/Нет)\n"
                        "Ваш ответ: ")).lower()

        while ans == "да":
            await delete_tables()
            ans = str(input("Удалить заказы за другим столиком? (Да/Нет)\n"
                            "Ваш ответ: ")).lower()


async def generate_order_send_kitchen(table: int) -> None:
    count = int(input("\nУкажите количество заказов: "))
    await get_price_list()

    start_time = time.time()
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(count):
            tasks.append(create_and_send_order(client, table, i))

        await asyncio.gather(*tasks)

    # end_time = time.time()
    # elapsed_time = round((end_time - start_time), 2)
    # print(f"{count} заказ(ов) созданы и отправлены на кухню за {elapsed_time} сек.")
    print(f"{count} заказ(ов) созданы и отправлены на кухню")

    answer = int(input("\n1. Продолжить работу\n"
                       "2. Закончить\n"
                       "Ваш выбор: "))

    if answer == 1:
        await select()
    elif answer == 2:
        print("Работа метода завершена")


async def create_and_send_order(client: httpx.AsyncClient, table: int, index: int) -> None:
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
        headers=header
    )
    sale_response.raise_for_status()
    sale_data = sale_response.json()
    sale = sale_data['result']['d'][0]
    # sale_list.append(sale)

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
                # "Sale": sale_list[index],
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
        }
    )
    add_response.raise_for_status()
    add_data = add_response.json()
    sale_order = add_data["result"]["d"][0][1]
    # sale_nom_list.append(sale_order)

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
        }
    )


async def main():
    await select()


if __name__ == "__main__":
    asyncio.run(main())