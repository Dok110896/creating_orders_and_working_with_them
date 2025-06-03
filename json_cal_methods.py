import datetime
import random
import uuid
from config import *


# Авторизация offline
def auth_off():
    return {
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


def auth_only():
    return {
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


# Получить настройки
def retail_getinitsettings():
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Retail.GetInitialSettings",
        "params": {
            "Product": 2
        },
        "id": 1
    }


# Получить информацию о клиенте
def get_userinfo():
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Пользователь.GetCurrentUser",
        "params": {},
        "id": 1
    }


# Список столиков
def prestosale_list():
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "PrestoSale.List",
        "params": {
            "Фильтр": {
                "d": ["Location", company, str(datetime.datetime.now().strftime("%Y-%m-%d")), hall, active_scheme,
                      "orders", active_scheme, None, True, 4, warehouse, True],
                "s": [{
                    "t": "Строка",
                    "n": "AggField"
                }, {
                    "t": "Число целое",
                    "n": "company"
                }, {
                    "t": "Строка",
                    "n": "Date"
                }, {
                    "t": "Число целое",
                    "n": "Hall"
                }, {
                    "t": "Число целое",
                    "n": "Id"
                }, {
                    "t": "Строка",
                    "n": "Mode"
                }, {
                    "t": "Число целое",
                    "n": "Scheme"
                }, {
                    "t": "Строка",
                    "n": "Seller"
                }, {
                    "t": "Логическое",
                    "n": "SingleHall"
                }, {
                    "t": "Число целое",
                    "n": "Version"
                }, {
                    "t": "Число целое",
                    "n": "Warehouse"
                }, {
                    "t": "Логическое",
                    "n": "WithPlan"
                }],
                "_type": "record",
                "f": 0
            },
            "Сортировка": None,
            "Навигация": None,
            "ДопПоля": ["*"]
        },
        "id": 1
    }


# Создать продажу
def sale_create(table):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Sale.Create",
        "params": {
            "Params": {
                "d": [
                    company,
                    {"workplace": workplace,
                     "product": 2},
                    table,
                    "order",
                    price_list,
                    0,
                    True
                ],
                "s": [
                    {"t": "Число целое", "n": "company"},
                    {"t": "JSON-объект", "n": "Properties"},
                    {"t": "Число целое", "n": "Location"},
                    {"t": "Строка", "n": "Reglament"},
                    {"t": "Число целое", "n": "PriceList"},
                    {"t": "Число целое", "n": "Type"},
                    {"t": "Логическое", "n": "ReturnSellerInfo"}
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }


# Получить номенклатуры по прайсу
def fastmenu_list():
    return {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "FastMenu.List",
        "params": {
            "Фильтр": {
                "d": [False, company, 4, company, str(datetime.datetime.now()), None, True, False, False, True, True, False,
                      "tile", "infinity", price_list, 11, [], warehouse],
                "s": [{"t": "Логическое", "n": "ActualRest"},
                      {"t": "Число целое", "n": "BalanceForOrganization"},
                      {"t": "Число целое", "n": "ColumnCount"},
                      {"t": "Число целое", "n": "company"},
                      {"t": "Строка", "n": "DateTime"},
                      {"t": "Строка", "n": "Folder"},
                      {"t": "Логическое", "n": "IsAddStopList"},
                      {"t": "Логическое", "n": "IsFlat"},
                      {"t": "Логическое", "n": "IsHeadExists"},
                      {"t": "Логическое", "n": "IsSeparateFolders"},
                      {"t": "Логическое", "n": "IsWideHead"},
                      {"t": "Логическое", "n": "IsWithModifiers"},
                      {"t": "Строка", "n": "Mode"},
                      {"t": "Строка", "n": "NavigationView"},
                      {"t": "Число целое", "n": "PriceList"},
                      {"t": "Число целое", "n": "RowCount"},
                      {"t": {"n": "Массив", "t": "Строка"},
                       "n": "UUIDsExclude"},
                      {"t": "Число целое", "n": "Warehouse"}], "_type": "record",
                "f": 0},
            "Сортировка": None,
            "Навигация": {"d": [True, 33, 0],
                          "s": [{"t": "Логическое", "n": "ЕстьЕще"},
                                {"t": "Число целое", "n": "РазмерСтраницы"},
                                {"t": "Число целое", "n": "Страница"}], "_type": "record",
                          "f": 0},
            "ДопПоля": ["Certificates", "DocumentPrintOptions", "DraughtType"]},
        "id": 1}


# Добавление позиции в продажу
def salenomenclature_addbatch(sale, nomenclature):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "SaleNomenclature.AddBatch",
        "params": {
            "Options": {
                "skip_sale_check": True,
                "pay_type": 0,
                "skip_calories": True
            },
            "Sale": sale,
            "Batch": {
                "d": [
                    [
                        str(uuid.uuid4()),
                        None,
                        None,
                        nomenclature,
                        None,
                        price_list,
                        random.randint(1, 20),
                        {
                            "type_ticket": None,
                            "origin_quantity": 1,
                            "skip_serial": None
                        }
                    ]
                ],
                "s": [
                    {"t": "UUID", "n": "RecordKey"},
                    {"t": "UUID", "n": "FolderKey"},
                    {"t": "UUID", "n": "Key"},
                    {"t": "Число целое", "n": "Nomenclature"},
                    {"t": "Деньги", "n": "ManualPrice"},
                    {"t": "Деньги", "n": "CatalogPrice"},
                    {"t": "Число вещественное", "n": "Quantity"},
                    {"t": "JSON-объект", "n": "Properties"}
                ],
                "_type": "recordset",
                "f": 0
            }
        },
        "id": 1
    }


# Отправка на готовку
def kitchen_setstate(sale_order, sale, table):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Kitchen.SetState",
        "params": {
            "rec": {
                "d": [
                    5, warehouse,
                    {
                        "d": [
                            [sale_order, None, None, sale, 0]
                        ],
                        "s": [
                            {"t": "Число целое", "n": "SaleNomenclature"},
                            {"t": "Число целое", "n": "ProductionNomenclatureQueue"},
                            {"t": "Число целое", "n": "State"},
                            {"t": "Число целое", "n": "Sale"},
                            {"t": "Число целое", "n": "Priority"}
                        ],
                        "_type": "recordset",
                        "f": 1
                    },
                    company,
                    table
                ],
                "s": [
                    {"t": "Число целое", "n": "State"},
                    {"t": "Число целое", "n": "Warehouse"},
                    {"t": "Выборка", "n": "SaleNomenclatures"},
                    {"t": "Число целое", "n": "company"},
                    {"t": "Число целое", "n": "Location"}
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }


def kitchen_task_list():
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Kitchen.TaskList",
        "params": {
            "Фильтр": {
                "d": [False, company, True, "in_work",
                      [str(datetime.datetime.now()), str(datetime.datetime.now())],
                      [None], None, True, [0, 5, 10], [warehouse]],
                "s": [
                    {"t": "Логическое", "n": "ByNomenclature"},
                    {"t": "Число целое", "n": "Company"},
                    {"t": "Логическое", "n": "IsOnline"},
                    {"t": "Строка", "n": "Mode"},
                    {"t": {"n": "Массив", "t": "Дата"}, "n": "Period"},
                    {"t": {"n": "Массив", "t": "Строка"}, "n": "ProductionSites"},
                    {"t": "Строка", "n": "Search"},
                    {"t": "Логическое", "n": "ShowDelivery"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "States"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "Warehouses"}
                ],
                "_type": "record",
                "f": 0
            },
            "Сортировка": {"d": [[False, "Started", True]]},
            "Навигация": {"d": [True, 999, 0]},
            "ДопПоля": []
        },
        "id": 1
    }


# Отметить блюдо готовым
def set_pnq_state(pnq, state):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "ProductionNomenclatureQueue.SetState",
        "params": {
            "Param": {
                "d": [[company], [pnq], state],
                "s": [
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "Companies"},
                    {"t": {"n": "Массив", "t": "Число целое"}, "n": "ProductionNomenclatureQueues"},
                    {"t": "Число целое", "n": "State"}
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }


# Получаем информацию о заказе на столике
def sale_restorememo(table):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Sale.RestoreMemo",
        "params": {
            "Params": {
                "d": [None, table, True, None, False, False, True, True],
                "s": [
                    {"t": "Число целое", "n": "Workplace"},
                    {"t": "Число целое", "n": "Location"},
                    {"t": "Логическое", "n": "ShowDiscounts"},
                    {"t": "Число целое", "n": "PriceList"},
                    {"t": "Логическое", "n": "ReversePositions"},
                    {"t": "Логическое", "n": "CreateSale"},
                    {"t": "Логическое", "n": "ShowGuests"},
                    {"t": "Логическое", "n": "ShowTables"}
                ],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }


# Удалить заказ
def delete_orders(sale_id, cause):
    return {
        "jsonrpc": "2.0",
        "protocol": 6,
        "method": "Sale.Cancel",
        "params": {
            "Sale": sale_id,
            "RefusalReason": cause,
            "Workplace": None,
            "AuthInfo": None,
            "Params": {
                "d": [True],
                "s": [{"t": "Логическое", "n": "CheckUnfinishedTasks"}],
                "_type": "record",
                "f": 0
            }
        },
        "id": 1
    }


# Блок оплаты заказа
def salerecalc(types, sale):
    return {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "Sale.Recalc",
        "params": {
            "Params": {"d": [types, 4, False, True, True, True, True, True, None, False],
                       "s": [{"t": "Число целое", "n": "PayType"},
                             {"t": "Число целое", "n": "PayMethod"},
                             {"t": "Логическое", "n": "WithoutApply"},
                             {"t": "Логическое", "n": "ShowPositions"},
                             {"t": "Логическое", "n": "ShowDiscounts"},
                             {"t": "Логическое", "n": "ShowOnlyChanged"},
                             {"t": "Логическое", "n": "UseInvoke"},
                             {"t": "Логическое", "n": "ShowPrompts"},
                             {"t": "Число целое", "n": "Customer"},
                             {"t": "Логическое", "n": "SkipPurchaseSend"}], "_type": "record", "f": 0},
            "Sale": sale}, "id": 1}


def sale_check(sale, workplace):
    return {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "Sale.Check",
        "params": {"Sale": sale,
                   "Params": {
                       "d": [True, True, True, True, True, False, True, workplace],
                       "s": [{"t": "Логическое", "n": "ReturnDeficit"},
                             {"t": "Логическое", "n": "CheckRest"},
                             {"t": "Логическое", "n": "CheckTotal"},
                             {"t": "Логическое", "n": "CheckUnfinishedTask"},
                             {"t": "Логическое", "n": "CheckErrorTasks"},
                             {"t": "Логическое", "n": "CheckDeliveryMinSum"},
                             {"t": "Логическое", "n": "CheckDynamicPositions"},
                             {"t": "Число целое", "n": "Workplace"}], "_type": "record", "f": 0}}, "id": 1}


def retail_sale_doc_get_gift_list(sale, sale_order, nomenclature, quantity, cost):
    return {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "RetailSaleDoc.GetGiftList",
        "params": {
            "SaleId": sale,
            "PositionList": {
                "d": [[sale_order, nomenclature, quantity, {"base": {"abbr": "шт", "code": "796", "name": "Штука", "qty": 1}}, None, cost]],
                "s": [{"t": "Число целое", "n": "PosId"},
                      {"t": "Число целое", "n": "NomId"},
                      {"t": "Число вещественное", "n": "Quantity"},
                      {"t": "JSON-объект", "n": "Package"},
                      {"t": "Деньги", "n": "FactCost"},
                      {"t": "Деньги", "n": "PlanCost"}],
                "_type": "recordset",
                "f": 0},
            "Params": {
                "d": [str(datetime.datetime.now()), warehouse, None, None, company, True, None],
                "s": [{"t": {"n": "Дата и время", "tz": False}, "n": "DateTime"},
                      {"t": "Число целое", "n": "WarehouseId"},
                      {"t": "Число целое", "n": "Customer"},
                      {"t": "Число целое", "n": "DeliveryType"},
                      {"t": "Число целое", "n": "SalePoint"},
                      {"t": "Логическое", "n": "WithUnavailable"},
                      {"t": {"n": "Массив", "t": "Число целое"}, "n": "Source"}], "_type": "record",
                "f": 0}}, "id": 1}


def sale_splitlist(sale, workplace):
    return {
        "jsonrpc": "2.0",
        "protocol": 7,
        "method": "Sale.SplitList",
        "params": {
            "Фильтр": {"d": [True, True, sale, [], workplace],
                       "s": [{"t": "Логическое", "n": "FlatMode"},
                             {"t": "Логическое",
                              "n": "ForceNomenclatureInfo"},
                             {"t": "Число целое", "n": "Sale"},
                             {"t": {"n": "Массив", "t": "Строка"},
                              "n": "SkipTaxSystemKKM"},
                             {"t": "Число целое",
                              "n": "Workplace"}], "_type": "record",
                       "f": 0}, "Сортировка": None,
            "Навигация": None, "ДопПоля": []}, "id": 1}


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
                      {"d": ["", None, False, None, None, None, None, False, None, False, None, False, None, None, True, True, True, False,
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
                       "s": [{"t": "Число целое", "n": "Device"}, {"t": "Число целое", "n": "company"},
                             {"t": "Логическое", "n": "Autonomous"},
                             {"t": "Строка", "n": "TID"}, {"t": "Число целое", "n": "PaymentType"}], "_type": "recordset", "f": 4}, {"d": [
                        # SaleNomenclatures
                        [None, None, False, None, None, None, None, None, None, self.catalogprice, None, self.checkprice, self.checksum,
                         None,
                         False, None, False, None, None, 1, None,
                         False, self.key_nom, None, None, None, self.nom_name, self.nom_order, 4, None, 0,
                         None, {"base": {"abbr": self.abbr, "code": self.code, "name": self.base_name, "qty": 1}}, None, None, None, None,
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
                              {"t": "Строка", "n": "CodeTRU"}, {"t": "Логическое", "n": "Excisable"}, {"t": "Число целое", "n": "Folder"},
                              {"t": "Логическое", "n": "Folder@"}, {"t": "UUID", "n": "FolderKey"}, {"t": "Число целое", "n": "FolderType"},
                              {"t": "Число вещественное", "n": "Fraction"}, {"t": "Строка", "n": "FullNumber"},
                              {"t": "Логическое", "n": "IsKit"},
                              {"t": "UUID", "n": "Key"}, {"t": "Число целое", "n": "KitSettings"}, {"t": "Деньги", "n": "ManualPrice"},
                              {"t": "Запись", "n": "MarkingInfo"}, {"t": "Строка", "n": "Name"}, {"t": "Число целое", "n": "Nomenclature"},
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
                                     {"n": "TotalPrice", "t": {"n": "Деньги", "p": 2}}, {"n": "FolderPrice", "t": {"n": "Деньги", "p": 2}},
                                     {"n": "UnitPrice", "t": {"n": "Деньги", "p": 2}}, {"n": "TotalVAT", "t": {"n": "Деньги", "p": 2}},
                                     {"n": "TaxRate", "t": "Число целое"}, {"n": "VATRate", "t": "Число вещественное"},
                                     {"n": "TaxRatePrepayment", "t": "Число целое"}, {"n": "VATRatePrepayment", "t": "Число вещественное"},
                                     {"n": "Printable", "t": "Логическое"}], "_type": "recordset", "f": 7},
                              self.closed, self.maincompany, self.prepaySum, self.totalcertificate, None, False]],
                       "s": [{"n": "Id", "t": "Строка"}, {"n": "Folder", "t": "Строка"}, {"n": "Folder@", "t": "Логическое"},
                             {"n": "Name", "t": "Строка"}, {"n": "KKM", "t": "Число целое"},
                             {"n": "company", "t": "Число целое"}, {"n": "companyINN", "t": "Строка"},
                             {"n": "Realcompany", "t": "Число целое"}, {"n": "Warehouse", "t": "Число целое"},
                             {"n": "TaxSystemCode", "t": "Число целое"}, {"n": "TaxSystemName", "t": "Строка"},
                             {"n": "VATPayer", "t": "Логическое"}, {"n": "Amount", "t": {"n": "Деньги", "p": 2}},
                             {"n": "Alcohol", "t": "Логическое"}, {"n": "MarkedAlcohol", "t": "Логическое"},
                             {"n": "Positions", "t": "Выборка"}, {"n": "Closed", "t": "Логическое"},
                             {"n": "Maincompany", "t": "Логическое"}, {"n": "PrePaySum", "t": {"n": "Деньги", "p": 2}},
                             {"n": "TotalCertificate", "t": {"n": "Деньги", "p": 2}},
                             {"t": "Логическое", "n": "ForPrepayment"}, {"t": "Логическое", "n": "InProcess"}],
                       "_type": "recordset", "r": {"f": 0,
                                                   "d": [None, None, None, None, None, None, None, None, None, None, None, None,
                                                         self.amount,
                                                         None, None, None, None, None, None, None],
                                                   "s": [{"n": "Id", "t": "Строка"}, {"n": "Folder", "t": "Строка"},
                                                         {"n": "Folder@", "t": "Логическое"}, {"n": "Name", "t": "Строка"},
                                                         {"n": "KKM", "t": "Число целое"}, {"n": "company", "t": "Число целое"},
                                                         {"n": "companyINN", "t": "Строка"}, {"n": "Realcompany", "t": "Число целое"},
                                                         {"n": "Warehouse", "t": "Число целое"}, {"n": "TaxSystemCode", "t": "Число целое"},
                                                         {"n": "TaxSystemName", "t": "Строка"}, {"n": "VATPayer", "t": "Логическое"},
                                                         {"n": "Amount", "t": {"n": "Деньги", "p": 2}}, {"n": "Alcohol", "t": "Логическое"},
                                                         {"n": "MarkedAlcohol", "t": "Логическое"}, {"n": "Positions", "t": "Выборка"},
                                                         {"n": "Closed", "t": "Логическое"}, {"n": "Maincompany", "t": "Логическое"},
                                                         {"n": "PrePaySum", "t": {"n": "Деньги", "p": 2}},
                                                         {"n": "TotalCertificate", "t": {"n": "Деньги", "p": 2}}], "_type": "record"},
                       "f": 6}, None, None],
                "s": [{"t": "UUID", "n": "Key"}, {"t": "Число целое", "n": "Sale"}, {"t": "Число целое", "n": "Number"},
                      {"t": "Число целое", "n": "Type"}, {"t": "Число целое", "n": "Customer"}, {"t": "Деньги", "n": "Amount"},
                      {"t": "Деньги", "n": "TotalPrice"}, {"t": "Деньги", "n": "TotalDiscount"}, {"t": "Строка", "n": "Comment"},
                      {"t": "Число целое", "n": "Source"}, {"t": "Дата и время", "n": "Created"}, {"t": "JSON-объект", "n": "Properties"},
                      {"t": "Число целое", "n": "TaxSystemCode"}, {"t": "Деньги", "n": "CashTotalSum"},
                      {"t": "Деньги", "n": "EcashTotalSum"},
                      {"t": "Запись", "n": "EcashSubSums"}, {"t": "Деньги", "n": "PrepaidSum"}, {"t": "Деньги", "n": "CreditSum"},
                      {"t": "Деньги", "n": "ProvisionSum"}, {"t": "Запись", "n": "PrepaidQualification"}, {"t": "Число целое", "n": "KKM"},
                      {"t": "Число целое", "n": "PaymentType"}, {"t": "Число целое", "n": "BankType"},
                      {"t": "Запись", "n": "CarryParameters"},
                      {"t": "Выборка", "n": "PaymentTerminalList"}, {"t": "Выборка", "n": "SaleNomenclatures"},
                      {"t": "Выборка", "n": "SplitInfo"}, {"t": "JSON-объект", "n": "RetryParameters"}, {"t": "Выборка", "n": "AlcoMarks"}],
                "_type": "record", "f": 0}}, "id": 1}
