import psycopg2
from config.conf import Config
from datetime import date, timedelta


class Database:
    @property
    def connection(self):
        cfg = Config()
        return psycopg2.connect(
            database=cfg.dbase,
            user=cfg.user,
            password=cfg.password,
            host=cfg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_users(self, group: str):
        sql = '''
            SELECT restName, restId 
            FROM settings 
            WHERE restGroup=%s order by restId
        '''
        parameters = (group,)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_data(self, name: str):
        sql = '''
            SELECT restId, uuId, restLogin, restPassword, countryCode 
            FROM settings 
            WHERE restName=%s
        '''
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_line(self, dt: str, rest_id: int):
        sql = '''
            SELECT ordersDay, restId 
            FROM month 
            WHERE ordersDay=%s and restId=%s
        '''
        parameters = (dt, rest_id)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_metrics(self, dt: date, rest_id: int, name_rest: str, revenue: int, revenue_rest: int,
                    revenue_del: int, revenue_pick: int, stop: timedelta, del_time: timedelta,
                    cert: int, ord_h: float, time_d: timedelta, time_s: timedelta, time_r: timedelta,
                    time_w: float, prod: int, st: float, pr: float, ass: float, happy: str, product: str,
                    s: float, s_rest: float, s_del: float):
        sql = '''
            INSERT INTO month (ordersDay, restId, restName, revenue, revenueRest, revenueDelivery,
                        revenuePickup, stopSelling, speedDelivery, certificates, ordersHour, timeDelivery,
                        timeShelf, timeRest, workKitchen, productivity, ratingStandard, ratingProduct,
                        ratingAss, ratingHappy, productHour, sales, salesRest, salesDelivery)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s)
        '''
        params = (dt, rest_id, name_rest, revenue, revenue_rest, revenue_del, revenue_pick, stop, del_time,
                  cert, ord_h, time_d, time_s, time_r, time_w, prod, st, pr, ass, happy, product, s, s_rest, s_del)
        self.execute(sql, parameters=params, commit=True)
