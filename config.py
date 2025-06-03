from datetime import time as dt_time
"Авторизация"
"Данные по авторизации стенд, логин и пароль"
authEndpoint = "https://fix-sso.sbis.ru/auth/service/"
standEndpoint = "https://fix-online.sbis.ru/service/"
user = 'dp_sp11_96'
password = '1108Denis@'


hall = 4603
active_scheme = 4604
workplace = 51

"Номенклатуры из прайса"
menu = [161, 159, 165, 163, 164, 158, 160, 162, 412, 418, 416, 409, 414, 411, 413, 420, 767, 763, 765, 771, 768,
                                   772, 779, 776, 878, 861, 864, 872, 634, 633, 636, 631, 632, 638, 630, 635, 637, 629, 3282, 3613]

# authEndpoint = "http://127.0.0.1:7071/auth/service/"
# standEndpoint = "http://127.0.0.1:7071/PrestoOffline/service/"
url_plugin = 'http://127.0.0.1:7071/service/?pool=SaleMobilePlugin'

table_num = {
    0: 0,  # чтоб билось по значению добавлен 0
    1: 4605,
    2: 4938,
    3: 4939,
    4: 4940}

"Метод FastMenu.List"
company = 3395
price_list = 10
warehouse = 3397

"Sale.Create"
product = 2

"SaleNomenclature.AddBatch"
nomenclature = 159
quantity = 10
catalog_price = 60

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
