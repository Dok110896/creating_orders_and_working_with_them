import asyncio

import httpx
from user_settings import *

async def auth_fix():
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                authEndpoint,
                json={
                    "jsonrpc": "2.0",
                    "method": "СБИС.Аутентифицировать",
                    "params": {
                        "Параметр": {
                            "Логин": user,
                            "Пароль": password
                        }
                    },
                    "id": 0
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get('result')
    except Exception as e:
        print(f"Auth error: {str(e)}")
        return None

header = {
    "Content-Type": "application/json; charset=utf-8",
    "X-SBISSessionID": asyncio.run(auth_fix())
}