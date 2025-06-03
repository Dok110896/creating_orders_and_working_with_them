import requests
from date import *
from json_cal_methods import auth, fastmenu_list
from config import *

# authEndpoint = "http://127.0.0.1:7071/auth/service/"
# standEndpoint = "http://127.0.0.1:7071/PrestoOffline/service/"
# url_plugin = 'http://127.0.0.1:7071/service/?pool=SaleMobilePlugin'
authEndpoint = "https://fix-sso.sbis.ru/auth/service/"
standEndpoint = "https://fix-online.sbis.ru/service/"


def auth_fix():
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
        response = requests.post(
            authEndpoint,
            headers=headers,
            # для авторизации оффлайн
            # json=json_sap
            # для авторизации на онлайне
            json=sbis_auth,
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
    "X-SBISSessionID": auth_fix()}

response = requests.post(standEndpoint, json=fastmenu_list(), headers=header).json()
# menu = response['result']['d']
menu_list = {}

for item in response['result']['d']:
    key = item[19]
    value = item[43]
    menu_list[key] = value
print(menu_list.keys())
# menus = [161, 159, 165, 163, 164, 158, 160, 162, 412, 418, 416, 409, 414, 411, 413, 420, 767, 763, 765, 771, 768, 772, 779, 776, 878, 861,
#          864, 872, 634, 633, 636, 631, 632, 638, 630, 635, 637, 629, 3282, 3613]
# memo = {11656: 'Осборн Солера Бренди', 11658: 'Вальдеспино Солера Бренди', 11659: 'Торрес 10 Гран Резерва Бренди',
#         13019: 'Аперитив "Aperol" 0.7 л.', 13747: 'Арманьяк "Baron G. Legrand VS Bas Armagnac" 0.7 л.',
#         12288: 'Армянский коньяк "АНИ" 6 лет 0.5 л.', 17876: 'Баклажаны маринованные (100 г)', 17879: 'Ветчина (30гр)',
#         17971: 'Винегрет овощной 100гр (Яр)', 13882: 'Апельсиново - гвоздичный ликер п/ф на 1,0', 13883: 'Базиличелло п/ф',
#         13901: 'Джин на лаванде п/ф 1,0', 14451: 'Ароматизатор Фисташка', 14479: 'Булочка для гамбургера 100мм (50гр)',
#         14480: 'Булочка для гамбургера 125мм (80гр)', 25099: 'Говядина вырезка,зачищ.с/м', 25106: 'Каштаны очищ.',
#         25124: 'Краб (Консервы)дешев.', 25125: 'Сертификат 2.000 рублей', 25128: 'Сертификат 2.000 рублей (электронный)',
#         25126: 'Сертификат 3.000 рублей', 25095: 'Лекарственная номенклатура', 26603: 'Товар_мод_1', 25096: 'Прослеживаемая номенклатура',
#         6747: 'Сувениры', 24859: 'Вафли', 24864: 'Одноразовая посуда (тур поход)', 24867: 'Американо персонал', 24868: 'Аренда',
#         24869: 'Аренда зала "Контейнерная"', 24929: 'Dolfin D004 Ср-во для мытья полов',
#         24930: 'Dolfin D012 Ср-во для уборки сантехнических помещений', 24931: 'Dolfin D027-5 Средство для ручной мойки посуды 5л'}
# print(memo.keys())
