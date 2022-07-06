from postgres.psql import Database
from date_work import DataWork
from changer.reader import Reader
from changer.change import Changer
from datetime import date


def change_orders(group):
    db = Database()
    dt_end = DataWork(date_end=date(2022, 6, 30)).set_date()
    users = db.get_users(group)
    for user in users:
        line = db.get_line(dt_end, user[1])
        cls_df = Reader(user[0])
        cls_df.read_df()
        change = Changer(cls_df)
        revenue, revenue_rest, revenue_del, revenue_pick = change.change_revenue()
        stop_selling = change.change_being_stop()
        delivery_time, certificates, order_hour = change.change_delivery_statistic()
        time_in_delivery, time_in_shelf = change.change_handover_delivery()
        time_in_rest = change.change_handover_stationary()
        time_work = change.change_time_work()
        productivity = change.change_productivity(revenue, time_work)
        res_st, res_prod, res_ass, res_happy = change.change_rating()
        product = change.change_product()
        sales, sales_rest, sales_delivery = change.change_sales()
        if len(line) == 0:
            db.add_metrics(dt_end, user[1], user[0], revenue, revenue_rest, revenue_del, revenue_pick,
                           stop_selling, delivery_time, certificates, order_hour, time_in_delivery,
                           time_in_shelf, time_in_rest, time_work, productivity, res_st, res_prod,
                           res_ass, res_happy, product, sales, sales_rest, sales_delivery)
        else:
            db.update_metrics(dt_end, user[1], user[0], revenue, revenue_rest, revenue_del, revenue_pick,
                           stop_selling, delivery_time, certificates, order_hour, time_in_delivery,
                           time_in_shelf, time_in_rest, time_work, productivity, res_st, res_prod,
                           res_ass, res_happy, product)
