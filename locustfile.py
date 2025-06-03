# Запуск файла locust -f locustfile.py --host https://fix-presto.sbis.ru
import time
import random
from locust import HttpUser, task, between
from json_cal_methods import *
from loguru import logger
from config import *


class PrestoUser(HttpUser):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = None
        self.session_id = None
        self.headers = None
        # Выбор столика
        self.table = None
        # Создание заказа
        self.sale = None
        self.sale_key = None
        self.open_wtz = None
        self.product = None
        self.workplace = None
        # Добавление номенклатуры
        self.sale_order = None
        self.key_nom = None
        self.nom_order = None
        self.nom_category = None
        self.nom_name = None
        self.quantity = None
        self.unitcode = None
        self.unitname = None
        self.catalogprice = None
        self.checkprice = None
        self.checksum = None
        self.abbr = None
        self.code = None
        self.base_name = None
        # Отправка на готовку
        self.pnq = None
        # Пересчет
        self.totalprice = None
        # sale_splitlist
        self.id = None
        self.name_org = None
        self.kkm = None
        self.inn = None
        self.warehouse_org = None
        self.taxsystemcode = None
        self.taxsystemname = None
        self.vatpayer = None
        self.amount = None
        self.alcohol = None
        self.markedalcohol = None
        self.unitprice = None
        self.totalvat = None
        self.taxrate = None
        self.vatrate = None
        self.taxrateprepayment = None
        self.vatrateprepayment = None
        self.printable = None
        self.closed = None
        self.maincompany = None
        self.prepaySum = None
        self.totalcertificate = None

    def on_start(self):
        # Авторизация
        self.headers = {"Content-Type": "application/json; charset=utf-8",
                        "Accept": "application/json"}
        self.authorization()
        self.header = {**self.headers, "X-Session-ID": self.session_id}

    def authorization(self):
        response = self.client.post(
            authEndpoint,
            json=auth_only(),
            headers=self.headers)

        # Проверяем успешность запроса и получаем ИдСессии
        if response.status_code == 200:
            try:
                # self.session_id = response.json()['result']['d'][0][1]
                # получение id сессии облако
                data = response.json()
                self.session_id = response.json()['result']
                logger.success(f"Успешная авторизация. Session ID: {self.session_id}")
            except KeyError:
                logger.error("Не удалось получить ИдСессия из ответа!")
        else:
            logger.error(f"Ошибка авторизации: {response.status_code}")

    # Блок создания заказа
    def presto_sale_list(self):
        logger.info("Получаем список доступных столов для оформления заказа")
        response = self.client.post(
            standEndpoint,
            json=prestosale_list(),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

        tables = response.json()['result']['d']
        logger.info(f"Всего доступных столов - {len(tables)}")
        self.table = tables[random.randint(0, len(tables) - 1)][0]
        time.sleep(1)
        logger.info(f"Выбрали для заказа стол - {self.table}")

    def sale_create(self):
        logger.info(f"Создаем заказ за столом - {self.table}")
        response = self.client.post(
            standEndpoint,
            json=sale_create(self.table),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

        sale = response.json()['result']['d']
        self.sale = sale[0]  # Sale
        # self.sale_key = sale[2]  # Key
        # self.open_wtz = sale[4]  # OpenedWTZ
        # self.product = sale[25]['product']
        # self.workplace = sale[25]['workplace']
        logger.info(f"Создан заказ - №{self.sale}")

    def salenomenclature_addbatch(self):
        menus_fix = random.choice(menu)
        response = self.client.post(
            standEndpoint,
            json=salenomenclature_addbatch(sale=self.sale, nomenclature=menus_fix),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'
        sale_addbatch = response.json()["result"]["d"][0]

        self.sale_order = sale_addbatch[1]  # SaleNomenclature
        # self.key_nom = sale_addbatch[6]  # Key номенклатуры
        # self.nom_order = sale_addbatch[9]  # Nomenclature
        # self.nom_category = sale_addbatch[27]  # NomenclatureCategory
        self.nom_name = sale_addbatch[12]  # Name
        # self.unitcode = sale_addbatch[14]  # UnitCode
        # self.unitname = sale_addbatch[15]  # UnitName
        # self.catalogprice = sale_addbatch[19]  # CatalogPrice
        self.quantity = sale_addbatch[34]
        # self.checkprice = sale_addbatch[75]  # CheckSum
        # self.checksum = sale_addbatch[76]  # CheckDiscount
        # self.abbr = sale_addbatch[16]["base"]["abbr"]
        # self.code = sale_addbatch[16]["base"]["code"]
        # self.base_name = sale_addbatch[16]["base"]["name"]
        logger.info(f"Добавили в заказ номенклатуру {self.nom_name} в количестве {self.quantity}")

    # Блок отправки на готовку, отметка готовымБ проверка, что задание на кухне
    def kitchen_setstate(self):
        logger.info("Отправили блюдо на кухню")
        response = self.client.post(standEndpoint,
                                    json=kitchen_setstate(sale_order=self.sale_order, sale=self.sale, table=self.table),
                                    headers=self.header)
        assert response.status_code == 200, 'Метод падает'
        self.pnq = response.json()["result"]["d"][0][0]

    def check_ready(self):
        logger.info("Отмечаем блюдо готовым на кухне")
        response = self.client.post(
            standEndpoint,
            json=set_pnq_state(pnq=self.pnq, state=10),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def check_served(self):
        logger.info("Отмечаем блюдо поданным")
        response = self.client.post(
            standEndpoint,
            json=set_pnq_state(pnq=self.pnq, state=15),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def check_in_work(self):
        logger.info("Отмечаем блюдо в работу")
        response = self.client.post(
            standEndpoint,
            json=set_pnq_state(pnq=self.pnq, state=5),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def delete_orders_from_tables(self):
        cause = {
            1: "Перепутали наименование",
            2: "Случайный выбор",
            3: "Не устраивает качество",
            4: "Проверка цены",
            5: "Не устроила цена",
            8: "Проблемный код маркировки",
            9: "Истекший срок годности"}
        cause_keys = list(cause.keys())
        cause_info = random.choice(cause_keys)
        logger.info(f"Удаляем заказ со столика с причиной - {cause.get(cause_info)}")

        response = self.client.post(
            standEndpoint,
            json=delete_orders(self.sale, cause=cause_info),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def sale_restorememo(self):
        logger.info(f"Проверяем, что заказ: {self.sale_order} был удален со столика {self.table}")
        response = self.client.post(
            standEndpoint,
            json=sale_restorememo(self.table),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

        orders_list = response.json()['result']['d']
        for item in orders_list:
            if item[0] != self.sale_order:
                logger.info("Заказ со столика успешно удален")
            else:
                logger.info("Заказ не был удален")

    # Блок оплаты заказа
    def sale_recalc(self, types):
        logger.info(f"Пересчитываем стоимость заказа {self.sale}")
        response = self.client.post(
            standEndpoint,
            json=salerecalc(types=types, sale=self.sale),
            headers=self.header
        )
        assert response.status_code == 200, 'Метод падает'
        self.totalprice = response.json()['result']['d'][0]
        logger.info(f"Стоимость блюд на столике составила {self.totalprice} рублей")

    def sale_check(self):
        logger.info("Производим проверку перед оплатой")
        response = self.client.post(
            standEndpoint,
            json=sale_check(self.sale, self.workplace),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def sale_splitlist(self):
        logger.info("Вызов метода Sale.SplitList")
        response = self.client.post(
            standEndpoint,
            json=sale_splitlist(sale=self.sale, workplace=self.workplace),
            headers=self.header)
        assert response.status_code == 200, 'Метод падает'

        split = response.json()['result']['d'][0]
        self.id = split[0]
        self.name_org = split[3]
        self.kkm = split[4]
        self.inn = split[6]
        self.warehouse_org = split[8]
        self.taxsystemcode = split[9]
        self.taxsystemname = split[10]
        self.vatpayer = split[11]
        self.amount = split[12]
        self.alcohol = split[13]
        self.markedalcohol = split[14]
        self.unitprice = split[15]['d'][0][4]
        self.totalvat = split[15]['d'][0][5]
        self.taxrate = split[15]['d'][0][6]
        self.vatrate = split[15]['d'][0][7]
        self.taxrateprepayment = split[15]['d'][0][8]
        self.vatrateprepayment = split[15]['d'][0][9]
        self.printable = split[15]['d'][0][10]
        self.closed = split[16]
        self.maincompany = split[17]
        self.prepaySum = split[18]
        self.totalcertificate = split[19]

    def sale_facade_pay(self, cashtotalsum, ecashtotalsum, bankcardsum):
        return {
            "jsonrpc": "2.0",
            "protocol": 7,
            "method": "SaleFacade.Pay",
            "params":
                {"Args": {
                    "d": [self.sale_key, self.sale, self.sale, 0, None, self.amount, self.totalprice, 0, "", None, self.open_wtz,
                          # Properties
                          {"product": self.product, "workplace": self.workplace, "email": "", "financial_doc": None},
                          None,
                          cashtotalsum, ecashtotalsum,
                          # Ecashsubsums
                          {"d": [bankcardsum, 0, 0, 0, None, None, None],
                           "s": [{"t": "Деньги",
                                  "n": "BankCardSum"},
                                 {"t": "Деньги",
                                  "n": "SalarySum"},
                                 {"t": "Деньги",
                                  "n": "QrCodeSum"},
                                 {"t": "Деньги",
                                  "n": "InternetSum"},
                                 {"t": "Деньги",
                                  "n": "PaymentOrderSum"},
                                 {"t": "Деньги",
                                  "n": "PreferentialCertificateSum"},
                                 {"t": "Выборка",
                                  "n": "UserSums"}],
                           "_type": "record", "f": 1}, 0, 0, 0,
                          # PrepaidQualification:
                          {"d": [0], "s": [{"t": "Деньги", "n": "CertificateSum"}], "_type": "record", "f": 2}, None, 4, None,
                          # Carryparametrs
                          {"d": ["", None, False, None, None, None, None, False, None, False, None, False, None, None, True, True, True,
                                 False,
                                 None],
                           "s": [{"t": "Строка", "n": "Comment"}, {"t": "Число целое", "n": "FinancialDoc"},
                                 {"t": "Логическое", "n": "IgnoreDynamicPositionsError"}, {"t": "Логическое", "n": "IsCredit"},
                                 {"t": "Логическое", "n": "IsFiscalSalary"}, {"t": "Логическое", "n": "IsNeedSplit"},
                                 {"t": "Логическое", "n": "IsOwnEmployee"}, {"t": "Логическое", "n": "IsZeroSalarySum"},
                                 {"t": "JSON-объект", "n": "LocationInfo"}, {"t": "Логическое", "n": "NonCashier"},
                                 {"t": "Логическое", "n": "NonFiscal"}, {"t": "Логическое", "n": "NonPaper"},
                                 {"t": "Строка", "n": "BasketId"}, {"t": "Строка", "n": "OriginalBasketId"},
                                 {"t": "Логическое", "n": "ShiftSyncForce"}, {"t": "Логическое", "n": "ShiftSyncNkkm"},
                                 {"t": "Логическое", "n": "UnusePaymentTerminal"}, {"t": "Логическое", "n": "UnuseUtm"},
                                 {"t": "Число целое", "n": "OwnerDoc"}], "_type": "record", "f": 3},
                          # PaymentTerminalList
                          {"d": [[None, company, True, None, None]],
                           "s": [{"t": "Число целое", "n": "Device"}, {"t": "Число целое", "n": "Company"},
                                 {"t": "Логическое", "n": "Autonomous"},
                                 {"t": "Строка", "n": "TID"}, {"t": "Число целое", "n": "PaymentType"}], "_type": "recordset", "f": 4},
                          {"d": [
                              # SaleNomenclatures
                              [None, None, False, None, None, None, None, None, None, self.catalogprice, None, self.checkprice,
                               self.checksum,
                               None,
                               False, None, False, None, None, 1, None,
                               False, self.key_nom, None, None, None, self.nom_name, self.nom_order, 4, None, 0,
                               None, {"base": {"abbr": self.abbr, "code": self.code, "name": self.base_name, "qty": 1}}, None, None, None,
                               None,
                               None, None, None, self.quantity,
                               None, None, self.sale_order, None, [], None, self.nom_name, None, 0, self.totalprice, None, None,
                               int(self.unitcode),
                               "шт", None]],
                              "s": [
                                  {"t": "Число вещественное", "n": "AlcoholBV"}, {"t": "Строка", "n": "AlcoholEGAIS"},
                                  {"t": "Логическое", "n": "AlcoholExcise"}, {"t": "Строка", "n": "AlcoholKind"},
                                  {"t": "Число вещественное", "n": "AlcoholVolume"}, {"t": "Число вещественное", "n": "AlcoholVolumeML"},
                                  {"t": "Строка", "n": "Barcode"}, {"t": "Число вещественное", "n": "Calories"},
                                  {"t": "Число вещественное", "n": "CaloriesPerUnit"}, {"t": "Деньги", "n": "CatalogPrice"},
                                  {"t": "Деньги", "n": "CheckCertificateTRU"}, {"t": "Деньги", "n": "CheckPrice"},
                                  {"t": "Деньги", "n": "CheckSum"},
                                  {"t": "Строка", "n": "CodeTRU"}, {"t": "Логическое", "n": "Excisable"},
                                  {"t": "Число целое", "n": "Folder"},
                                  {"t": "Логическое", "n": "Folder@"}, {"t": "UUID", "n": "FolderKey"},
                                  {"t": "Число целое", "n": "FolderType"},
                                  {"t": "Число вещественное", "n": "Fraction"}, {"t": "Строка", "n": "FullNumber"},
                                  {"t": "Логическое", "n": "IsKit"},
                                  {"t": "UUID", "n": "Key"}, {"t": "Число целое", "n": "KitSettings"}, {"t": "Деньги", "n": "ManualPrice"},
                                  {"t": "Запись", "n": "MarkingInfo"}, {"t": "Строка", "n": "Name"},
                                  {"t": "Число целое", "n": "Nomenclature"},
                                  {"t": "Число целое", "n": "NomenclatureCategory"}, {"t": "Строка", "n": "NomenclatureNumber"},
                                  {"t": "Число целое", "n": "NomenclatureKind"}, {"t": "UUID", "n": "NomenclatureUUID"},
                                  {"t": "JSON-объект", "n": "Package"}, {"t": "Строка", "n": "ParcelCode"},
                                  {"t": "JSON-объект", "n": "Properties"},
                                  {"t": "Число целое", "n": "Provider"}, {"t": "Строка", "n": "ProviderINN"},
                                  {"t": "Строка", "n": "ProviderName"},
                                  {"t": "Строка", "n": "ProviderPhone"}, {"t": "Число целое", "n": "ProviderType"},
                                  {"t": "Число вещественное", "n": "Quantity"}, {"t": "UUID", "n": "ReqId"},
                                  {"t": "Число целое", "n": "ReqTimestamp"},
                                  {"t": "Число целое", "n": "SaleNomenclature"}, {"t": "Строка", "n": "SerialNumber"},
                                  {"t": {"n": "Массив", "t": "Строка"}, "n": "SerialNumbers"}, {"t": "Число целое", "n": "SerialType"},
                                  {"t": "Строка", "n": "ShortName"}, {"t": "Число целое", "n": "TaxRate"},
                                  {"t": "Деньги", "n": "TotalDiscount"},
                                  {"t": "Деньги", "n": "TotalPrice"}, {"t": "Деньги", "n": "TotalVAT"}, {"t": "Строка", "n": "Unit"},
                                  {"t": "Число целое", "n": "UnitCode"}, {"t": "Строка", "n": "UnitName"},
                                  {"t": "Число целое", "n": "VATRate"}], "_type": "recordset", "f": 5},
                          # SplitInfo
                          {"d": [[self.id, None, None, self.name_org, self.kkm, company, self.inn, company, self.warehouse_org,
                                  self.taxsystemcode, self.taxsystemname, self.vatpayer, self.amount, self.alcohol, self.markedalcohol,
                                  {"d": [[self.sale_order, self.key_nom, self.totalprice, None, self.unitprice, self.totalvat,
                                          self.taxrate, self.vatrate, self.taxrateprepayment, self.vatrateprepayment, self.printable]],
                                   "s": [{"n": "SaleNomenclature", "t": "Число целое"}, {"n": "PositionKey", "t": "UUID"},
                                         {"n": "TotalPrice", "t": {"n": "Деньги", "p": 2}},
                                         {"n": "FolderPrice", "t": {"n": "Деньги", "p": 2}},
                                         {"n": "UnitPrice", "t": {"n": "Деньги", "p": 2}}, {"n": "TotalVAT", "t": {"n": "Деньги", "p": 2}},
                                         {"n": "TaxRate", "t": "Число целое"}, {"n": "VATRate", "t": "Число вещественное"},
                                         {"n": "TaxRatePrepayment", "t": "Число целое"},
                                         {"n": "VATRatePrepayment", "t": "Число вещественное"},
                                         {"n": "Printable", "t": "Логическое"}], "_type": "recordset", "f": 7},
                                  self.closed, self.maincompany, self.prepaySum, self.totalcertificate, None, False]],
                           "s": [{"n": "Id", "t": "Строка"}, {"n": "Folder", "t": "Строка"}, {"n": "Folder@", "t": "Логическое"},
                                 {"n": "Name", "t": "Строка"}, {"n": "KKM", "t": "Число целое"},
                                 {"n": "Company", "t": "Число целое"}, {"n": "CompanyINN", "t": "Строка"},
                                 {"n": "RealCompany", "t": "Число целое"}, {"n": "Warehouse", "t": "Число целое"},
                                 {"n": "TaxSystemCode", "t": "Число целое"}, {"n": "TaxSystemName", "t": "Строка"},
                                 {"n": "VATPayer", "t": "Логическое"}, {"n": "Amount", "t": {"n": "Деньги", "p": 2}},
                                 {"n": "Alcohol", "t": "Логическое"}, {"n": "MarkedAlcohol", "t": "Логическое"},
                                 {"n": "Positions", "t": "Выборка"}, {"n": "Closed", "t": "Логическое"},
                                 {"n": "MainCompany", "t": "Логическое"}, {"n": "PrePaySum", "t": {"n": "Деньги", "p": 2}},
                                 {"n": "TotalCertificate", "t": {"n": "Деньги", "p": 2}},
                                 {"t": "Логическое", "n": "ForPrepayment"}, {"t": "Логическое", "n": "InProcess"}],
                           "_type": "recordset", "r": {"f": 0,
                                                       "d": [None, None, None, None, None, None, None, None, None, None, None, None,
                                                             self.amount,
                                                             None, None, None, None, None, None, None],
                                                       "s": [{"n": "Id", "t": "Строка"}, {"n": "Folder", "t": "Строка"},
                                                             {"n": "Folder@", "t": "Логическое"}, {"n": "Name", "t": "Строка"},
                                                             {"n": "KKM", "t": "Число целое"}, {"n": "Company", "t": "Число целое"},
                                                             {"n": "CompanyINN", "t": "Строка"}, {"n": "RealCompany", "t": "Число целое"},
                                                             {"n": "Warehouse", "t": "Число целое"},
                                                             {"n": "TaxSystemCode", "t": "Число целое"},
                                                             {"n": "TaxSystemName", "t": "Строка"}, {"n": "VATPayer", "t": "Логическое"},
                                                             {"n": "Amount", "t": {"n": "Деньги", "p": 2}},
                                                             {"n": "Alcohol", "t": "Логическое"},
                                                             {"n": "MarkedAlcohol", "t": "Логическое"}, {"n": "Positions", "t": "Выборка"},
                                                             {"n": "Closed", "t": "Логическое"}, {"n": "MainCompany", "t": "Логическое"},
                                                             {"n": "PrePaySum", "t": {"n": "Деньги", "p": 2}},
                                                             {"n": "TotalCertificate", "t": {"n": "Деньги", "p": 2}}], "_type": "record"},
                           "f": 6}, None, None],
                    "s": [{"t": "UUID", "n": "Key"}, {"t": "Число целое", "n": "Sale"}, {"t": "Число целое", "n": "Number"},
                          {"t": "Число целое", "n": "Type"}, {"t": "Число целое", "n": "Customer"}, {"t": "Деньги", "n": "Amount"},
                          {"t": "Деньги", "n": "TotalPrice"}, {"t": "Деньги", "n": "TotalDiscount"}, {"t": "Строка", "n": "Comment"},
                          {"t": "Число целое", "n": "Source"}, {"t": "Дата и время", "n": "Created"},
                          {"t": "JSON-объект", "n": "Properties"},
                          {"t": "Число целое", "n": "TaxSystemCode"}, {"t": "Деньги", "n": "CashTotalSum"},
                          {"t": "Деньги", "n": "EcashTotalSum"},
                          {"t": "Запись", "n": "EcashSubSums"}, {"t": "Деньги", "n": "PrepaidSum"}, {"t": "Деньги", "n": "CreditSum"},
                          {"t": "Деньги", "n": "ProvisionSum"}, {"t": "Запись", "n": "PrepaidQualification"},
                          {"t": "Число целое", "n": "KKM"},
                          {"t": "Число целое", "n": "PaymentType"}, {"t": "Число целое", "n": "BankType"},
                          {"t": "Запись", "n": "CarryParameters"},
                          {"t": "Выборка", "n": "PaymentTerminalList"}, {"t": "Выборка", "n": "SaleNomenclatures"},
                          {"t": "Выборка", "n": "SplitInfo"}, {"t": "JSON-объект", "n": "RetryParameters"},
                          {"t": "Выборка", "n": "AlcoMarks"}],
                    "_type": "record", "f": 0}}, "id": 1}

    def salefacade_pay(self, cashtotalsum, ecashtotalsum, bankcardsum):
        response = self.client.post(url_plugin,
                                    json=self.sale_facade_pay(cashtotalsum=cashtotalsum,
                                                              ecashtotalsum=ecashtotalsum,
                                                              bankcardsum=bankcardsum),
                                    headers=self.header)
        assert response.status_code == 200, 'Метод падает'

    def set_type_payment(self):
        """
        Реализация случайного выбора способа оплаты: наличные и по карте
        :return:
        """
        for i in range(2):
            number = random.choice([1, 2])
            if number == 1:
                logger.info("Производим оплату наличными")
                self.sale_recalc(types=1)
                self.salefacade_pay(cashtotalsum=self.totalprice, ecashtotalsum=0, bankcardsum=0)
            elif number == 2:
                logger.info("Производим оплату по карте")
                self.sale_recalc(types=2)
                self.salefacade_pay(cashtotalsum=0, ecashtotalsum=self.totalprice, bankcardsum=self.totalprice)

    @task(3)    # 60% нагрузки (3/(3+1+1) = 0.6)
    def check_orders_served(self):
        self.presto_sale_list()
        self.sale_create()
        self.salenomenclature_addbatch()
        self.kitchen_setstate()
        self.wait()
        self.check_served()
        logger.info("Конец итерации")

    @task(1)    # 20% нагрузки (1/(3+1+1) = 0.2)
    def check_orders_ready(self):
        self.presto_sale_list()
        self.sale_create()
        self.salenomenclature_addbatch()
        self.kitchen_setstate()
        self.wait()
        self.check_ready()
        logger.info("Конец итерации")

    @task(1)    # 20% нагрузки (1/(3+1+1) = 0.2)
    def check_orders_in_work(self):
        self.presto_sale_list()
        self.sale_create()
        self.salenomenclature_addbatch()
        self.kitchen_setstate()
        self.wait()
        self.check_in_work()
        logger.info("Конец итерации")
