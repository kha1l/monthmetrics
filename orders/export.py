import requests
import fake_useragent
from datetime import date, timedelta
from postgres.psql import Database


class DataExportDay:

    def __init__(self, date_start: date, date_end: date, name: str):
        db = Database()
        data = db.get_data(name)
        self.name = name
        self.rest = data[0]
        self.uuid = data[1]
        self.date_end = date_end
        self.date_start = date_start
        self.login = data[2]
        self.password = data[3]
        self.code = data[4]
        self.session = None
        self.user = None
        self.header = None
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        log_data = {
            'CountryCode': self.code,
            'login': self.login,
            'password': self.password
        }
        self.header = {
            'user-agent': self.user
        }
        log_link = f'https://auth.dodopizza.{self.code}/Authenticate/LogOn'
        self.session.post(log_link, data=log_data, headers=self.header)

    def save(self, orders_data):
        for order in orders_data:
            response = self.session.post(orders_data[order]['link'], data=orders_data[order]['data'],
                                         headers=self.header)
            with open(f'./orders/export/{order}_{self.name}.xlsx', 'wb') as file:
                file.write(response.content)
                file.close()

    def save_prod(self, orders_data):
        for order in orders_data:
            response = self.session.post(orders_data[order]['link'], data=orders_data[order]['data'],
                                         headers=self.header)
            with open(f'./orders/export/{order}_{self.name}.txt', 'wb') as file:
                file.write(response.content)
                file.close()

    def product(self):
        orders_data = {
            'product': {
                'link': f'https://officemanager.dodopizza.{self.code}/OfficeManager/MonthlyStatistics/MonthlyStatisticsByDayPartial',
                'data': {
                    "selectedUnitId": self.rest,
                    "selectedMonth": self.date_end
                }
            }
        }
        self.save_prod(orders_data)

    def revenue(self):
        orders_data = {
            'revenue': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/Revenue/Export',
                'data': {
                    "unitsIds": self.rest,
                    "OrderSources": [
                        "Telephone",
                        "Site",
                        "Restaurant",
                        "Mobile",
                        "Pizzeria",
                        "Aggregator"
                    ],
                    "ReportType": "ByDates",
                    "reportType": "",
                    "pseudoBeginTime": "",
                    "pseudoBeginDate": self.date_start,
                    "pseudoEndTime": "",
                    "pseudoEndDate": self.date_end,
                    "beginDate": self.date_start,
                    "endDate": self.date_end,
                    "beginTime": "",
                    "endTime": "",
                    "date": self.date_end,
                    "IsVatIncluded": [
                        "true",
                        "false"
                    ],
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def delivery_statistic(self):
        orders_data = {
            'del_statistic': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/DeliveryStatistic/Export',
                'data': {
                    "unitsIds": self.rest,
                    "beginDate": self.date_start,
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)

    def being_stop(self):
        orders_data = {
            'being_stop': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/StopSaleStatistic/Export',
                'data': {
                    "UnitsIds": self.rest,
                    "stopType": "0",
                    "beginDate": self.date_start,
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)

    def handover_delivery(self):
        orders_data = {
            'handover-delivery': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/OrderHandoverTime/Export',
                'data': {
                    "unitsIds": self.uuid,
                    "beginDate": self.date_start,
                    "endDate": self.date_end,
                    "orderTypes": "Delivery",
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def handover_stationary(self):
        orders_data = {
            'handover_stationary': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/OrderHandoverTime/Export',
                'data': {
                    "unitsIds": self.uuid,
                    "beginDate": self.date_start,
                    "endDate": self.date_end,
                    "orderTypes": "Stationary",
                    "Export": "Экспорт+в+Excel"
                }
            }
        }
        self.save(orders_data)

    def time_work(self):
        orders_data = {
            'time_work': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/ActualTime/Export',
                'data': {
                    "PageIndex": "1",
                    "unitId": self.rest,
                    "EmployeeName": "",
                    "isGroupingByEmployee": [
                        "true",
                        "false"
                    ],
                    "beginDate": self.date_start,
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)

    def product_sales_delivery(self):
        orders_data = {
            'sales_delivery': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/ProductsSale/Export',
                'data': {
                    "unitsIds": self.rest,
                    "pizzeriaAge": "AnyAge",
                    "OrderSources": [
                        "Telephone",
                        "Site",
                        "Restaurant",
                        "DefectOrder",
                        "Mobile",
                        "Pizzeria",
                        "Aggregator"
                    ],
                    "orderTypeIds": [
                        "1",
                        "2"
                    ],
                    "beginDate": self.date_start,
                    "beginTime": "00:00",
                    "endDate": self.date_end,
                    "endTime": "23:59",
                    "excludeDate": "",
                    "radio-halves": "on",
                    "displayCombinationsHalves": "",
                    "radio-discount": "on",
                    "intervals": "on",
                    "displayInDays": [
                        "",
                        ""
                    ],
                    "timeInterval": "60",
                    "isExcludeHolidays": "",
                    "isExcludeWeekends": "",
                    "calculationWithDiscount": ""
                }
            }
        }
        self.save(orders_data)

    def product_sales_rest(self):
        orders_data = {
            'sales_rest': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/ProductsSale/Export',
                'data': {
                    "unitsIds": self.rest,
                    "pizzeriaAge": "AnyAge",
                    "OrderSources": [
                        "Telephone",
                        "Site",
                        "Restaurant",
                        "DefectOrder",
                        "Mobile",
                        "Pizzeria",
                        "Aggregator"
                    ],
                    "orderTypeIds": "3",
                    "beginDate": self.date_start,
                    "beginTime": "00:00",
                    "endDate": self.date_end,
                    "endTime": "23:59",
                    "excludeDate": "",
                    "radio-halves": "on",
                    "displayCombinationsHalves": "",
                    "radio-discount": "on",
                    "intervals": "on",
                    "displayInDays": [
                        "",
                        ""
                    ],
                    "timeInterval": "60",
                    "isExcludeHolidays": "",
                    "isExcludeWeekends": "",
                    "calculationWithDiscount": ""
                }
            }
        }
        self.save(orders_data)

    def product_sales(self):
        orders_data = {
            'sales': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/ProductsSale/Export',
                'data': {
                    "unitsIds": self.rest,
                    "pizzeriaAge": "AnyAge",
                    "OrderSources": [
                        "Telephone",
                        "Site",
                        "Restaurant",
                        "DefectOrder",
                        "Mobile",
                        "Pizzeria",
                        "Aggregator"
                    ],
                    "orderTypeIds": [
                        "1",
                        "2",
                        "3"
                    ],
                    "beginDate": self.date_start,
                    "beginTime": "00:00",
                    "endDate": self.date_end,
                    "endTime": "23:59",
                    "excludeDate": "",
                    "radio-halves": "on",
                    "displayCombinationsHalves": "",
                    "radio-discount": "on",
                    "intervals": "on",
                    "displayInDays": [
                        "",
                        ""
                    ],
                    "timeInterval": "60",
                    "isExcludeHolidays": "",
                    "isExcludeWeekends": "",
                    "calculationWithDiscount": ""
                }
            }
        }
        self.save(orders_data)
