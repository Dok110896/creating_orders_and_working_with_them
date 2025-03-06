from user_settings import *
import requests


def auth_fix():
    response_auth = requests.post(authEndpoint, json={
        "jsonrpc": "2.0",
        "method": "СБИС.Аутентифицировать",
        "params": {
            "Параметр": {
                "Логин": user,
                "Пароль": password
            }
        },
        "id": 0
    })

    response_data = response_auth.json()
    if 'result' in response_data:
        session = response_data['result']
        return session
    else:
        print("Authentication request failed. Response:", response_data)


header = {
    "Content-Type": "application/json",
    "X-SBISSessionID": auth_fix()}
