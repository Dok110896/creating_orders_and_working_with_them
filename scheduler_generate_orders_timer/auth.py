import requests

authEndpoint = "https://fix-sso.sbis.ru/auth/service/"
standEndpoint = "https://fix-online.sbis.ru/service/"
user = "dp_sp11_96"
password = "1108Denis@"


# Данные по столикам берем из метода PrestoSale номер столика и его id
table_num = {
    0: 0,  # чтоб билось по значению добавлен 0
    1: 4605,
    2: 4938,
    3: 4939,
    4: 4940
}

# Метод FastMenu.List. Проверить поле РазмерСтраницы
Company = 3395
ColumnCount = 7
PriceList = 10
RowCount = 13
Warehouse = 3397


# Sale.Create
Seller = 170
workplace = 22
product = 2

# SaleNomenclature.AddBatch
Nomenclature = 161
Quantity = 10
CatalogPrice = 60


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
