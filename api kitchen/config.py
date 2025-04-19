from datetime import datetime, time as dt_time
# Авторизация
# Данные по авторизации стенд, логин и пароль
authEndpoint = "https://fix-sso.sbis.ru/auth/service/"
standEndpoint = "https://fix-online.sbis.ru/service/"
user = "dp_sp11_96"
password = "1108Denis@"

# Данные для формирования продажи
# Данные по столикам берем из метода PrestoSale номер столика и его id
table_num = {
    0: 0,  # чтоб билось по значению добавлен 0
    1: 4605,
    2: 4938,
    3: 4939,
    4: 4940 }

# Метод FastMenu.List
Company = 3395
PriceList = 10
Warehouse = 3397

# Sale.Create
Seller = 170
workplace = 22
product = 2

# Из метода SaleNomenclature.AddBatch взять значение полей
Nomenclature = 159
Quantity = 10
CatalogPrice = 60

#  Для действий с конкретной датой
user_date = "2024-12-10"

# Настройка пакетной очереди отправки и удаления
MAX_CONCURRENT_REQUESTS = 50  # Лимит одновременных запросов в одной очереди
REQUEST_TIMEOUT = 30.0  # Таймаут для каждого запроса
MAX_CONCURRENT_DELETES = 50  # Лимит одновременных удалений в одной очереди
DELETE_TIMEOUT = 30.0  # Таймаут для каждого запроса
RETRY_ATTEMPTS = 3  # Количество попыток повтора
QUEUE_DELAY = 1  # Задержка между очередями в секундах

# Настройка шедулера
WORK_START = dt_time(7, 0) # Время начала запуска генерации очереди заказов
WORK_END = dt_time(19, 0) # Время завершения генерации очереди заданий
INTERVAL_MINUTES = 2 # Интервал через какое время будет созданы новые заказы
ORDERS_PER_BATCH = 10 # Количество создаваемых заказов в одну итерацию с отправкой на готовку
MAX_RETRIES = 3  # Максимальное количество попыток повтора запроса
DEFAULT_TABLE = 4  # Столик по умолчанию для шедулера индекс списка

