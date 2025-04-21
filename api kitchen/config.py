from datetime import time as dt_time
"Авторизация"
"Данные по авторизации стенд, логин и пароль"
authEndpoint = "https://fix-sso.sbis.ru/auth/service/"
standEndpoint = "https://fix-online.sbis.ru/service/"
user = None
password = None

table_num = {
    0: 0,  # чтоб билось по значению добавлен 0
    1: 4605,
    2: 4938,
    3: 4939,
    4: 4940}

"Метод FastMenu.List"
Company = 3395
PriceList = 10
Warehouse = 3397

"Sale.Create"
product = 2

"SaleNomenclature.AddBatch"
Nomenclature = 159
Quantity = 10
CatalogPrice = 60

"Для действий с конкретной датой"
user_date = "2024-12-10"

"Настройка пакетной очереди отправки и удаления"
MAX_CONCURRENT_REQUESTS = 50
REQUEST_TIMEOUT = 30.0
MAX_CONCURRENT_DELETES = 50
DELETE_TIMEOUT = 30.0
RETRY_ATTEMPTS = 3
QUEUE_DELAY = 1

"Настройка шедулера"
WORK_START = dt_time(10, 0)
WORK_END = dt_time(19, 0)
INTERVAL_MINUTES = 2
ORDERS_PER_BATCH = 10
MAX_RETRIES = 3
DEFAULT_TABLE = 4
