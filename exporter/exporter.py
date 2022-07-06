import time
from postgres.psql import Database
from date_work import DataWork
from orders.export import DataExportDay
from datetime import date


def save_orders(group):
    db = Database()
    dt_end = DataWork(date_end=date(2022, 6, 30)).set_date()
    dt_start = DataWork.get_month(dt_end)
    users = db.get_users(group)
    for user in users:
        data = DataExportDay(dt_start, dt_end, user[0])
        data.product()
        data.revenue()
        data.time_work()
        data.handover_delivery()
        data.handover_stationary()
        data.delivery_statistic()
        data.being_stop()
        data.product_sales_rest()
        data.product_sales_delivery()
        data.product_sales()
        time.sleep(5)
        print(user[0])
