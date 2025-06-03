from auth import *
from json_cal_methods import *
import asyncio
import httpx
import time


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
    start_time = time.time()
    async with httpx.AsyncClient(headers=header) as client:
        tasks = []
        for pnq in pnq_list:
            pnq_set_state_json = set_pnq_state(pnq=pnq, state=state)
            tasks.append(async_post(client, pnq_set_state_json))

        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    state_name = {
        10: "готовыми",
        15: "поданы",
        5: "в работу"
    }.get(state, "")
    print(f"Все заказы отмечены {state_name} за {elapsed_time} сек.")

async def check_ready():
    await set_pnq_state(10)

async def check_served():
    await set_pnq_state(15)
    # await verify_empty_kitchen()

async def check_in_work():
    await set_pnq_state(5)

async def verify_empty_kitchen():
    task_list_json = kitchen_task_list()

    async with httpx.AsyncClient(headers=header) as client:
        response = await async_post(client, task_list_json)
        if response:
            av = [row[18] for row in response['result']['d']]
            assert len(av) == 0, "На кухне остались блюда"

async def get_pnq_list():

    data = kitchen_task_list()

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

            result_data = response['result']

            if 'd' not in result_data:
                print("Ответ не содержит данных в 'd'")
                return []

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
