import asyncio
import httpx
from config import *


async def auth_fix():
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    try:
        # метод авторизации оффлайн
        json_sap = {
            "jsonrpc": "2.0",
            "protocol": 5,
            "method": "SAP.Authenticate",
            "params": {
                "data": {
                    "d": [user, password, True, None, False, None, True, True],
                    "s": [{
                        "t": "Строка",
                        "n": "login"
                    }, {
                        "t": "Строка",
                        "n": "password"
                    }, {
                        "t": "Логическое",
                        "n": "only_account"
                    }, {
                        "t": "Логическое",
                        "n": "stranger"
                    }, {
                        "t": "Логическое",
                        "n": "license_extended"
                    }, {
                        "t": "Строка",
                        "n": "license_session_id"
                    }, {
                        "t": "Логическое",
                        "n": "from_browser"
                    }, {
                        "t": "Логическое",
                        "n": "get_last_url"
                    }],
                    "_type": "record"
                }
            },
            "id": 1
        }
        # метод авторизации онлайн
        sbis_auth = {
                    "jsonrpc": "2.0",
                    "method": "СБИС.Аутентифицировать",
                    "params": {
                        "Параметр": {
                            "Логин": user,
                            "Пароль": password
                        }
                    },
                    "id": 0
                }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                authEndpoint,
                headers=headers,
                # для авторизации на онлайне
                json=sbis_auth,

                # для авторизации оффлайн
                # json=json_sap
            )
            response.raise_for_status()
            data = response.json()
            # получение id сессии облако
            return data.get('result')

            # получение id сессии оффлайн
            # return data['result']['d'][0][1]

    except Exception as e:
        print(f"Auth error: {str(e)}")
        return None

header = {
    "Content-Type": "application/json; charset=utf-8",
    "X-SBISSessionID": asyncio.run(auth_fix())
}
