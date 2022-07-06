from changer.reader import Reader
import pandas as pd
from datetime import timedelta
from bs4 import BeautifulSoup


class Changer:
    def __init__(self, obj: Reader) -> None:
        self.obj = obj

    @staticmethod
    def df_handover(df):
        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                t = timedelta(0)
            return t

        try:
            time_handover = pd.to_timedelta(
                df['Ожидание'].apply(change_time).mean() + df['Приготовление'].apply(change_time).mean())
        except KeyError:
            time_handover = '0:00:00'

        if issubclass(type(time_handover), pd._libs.tslibs.nattype.NaTType):
            time_handover = pd.to_timedelta(0)

        return time_handover

    @staticmethod
    def change_time(t):
        try:
            t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
        except AttributeError:
            t = timedelta(0)
        return t

    @staticmethod
    def change_string(t):
        t = str(t) + ':00'
        return t

    def change_revenue(self):
        df = self.obj.df_rev
        try:
            df = df.loc[df['Дата'] == 'Итого']
        except KeyError:
            df = pd.Dataframe()

        try:
            revenue = df.iloc[0]['Итого']
        except IndexError:
            revenue = 0
        except KeyError:
            revenue = 0

        try:
            revenue_rest = df.iloc[0]['Ресторан']
        except IndexError:
            revenue_rest = 0
        except KeyError:
            revenue_rest = 0

        try:
            revenue_del = df.iloc[0]['Доставка']
        except IndexError:
            revenue_del = 0
        except KeyError:
            revenue_del = 0

        try:
            revenue_pick = df.iloc[0]['Самовывоз']
        except IndexError:
            revenue_pick = 0
        except KeyError:
            revenue_pick = 0

        return int(revenue), int(revenue_rest), int(revenue_del), int(revenue_pick)

    def change_being_stop(self):
        df = self.obj.df_stop

        try:
            df = df.drop_duplicates(subset=['Дата остановки'], keep='first')
        except KeyError:
            df = 0

        try:
            stop_duration = pd.to_timedelta(df['Длительность за отчетный период'].apply(self.change_time).sum())
        except KeyError:
            stop_duration = 0

        return stop_duration

    def change_delivery_statistic(self):
        df = self.obj.df_del

        try:
            avg_del = df.iloc[0]['Среднее время доставки*']
        except IndexError:
            avg_del = timedelta(0)
        except KeyError:
            avg_del = timedelta(0)

        try:
            cert = df.iloc[0]['Количество просроченных заказов']
        except IndexError:
            cert = 0
        except KeyError:
            cert = 0

        try:
            ord_h = df.iloc[0]['Заказов на курьера в час']
        except IndexError:
            ord_h = 0
        except KeyError:
            ord_h = 0

        return avg_del, int(cert), float(ord_h)

    def change_handover_delivery(self):
        df = self.obj.df_hand_del

        def change_time(t):
            try:
                t = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
            except AttributeError:
                t = timedelta(0)
            return t

        try:
            time_shelf = pd.to_timedelta(df['Ожидание на полке'].apply(change_time).mean())
        except KeyError:
            time_shelf = timedelta(0)

        if issubclass(type(time_shelf), pd._libs.tslibs.nattype.NaTType):
            time_shelf = pd.to_timedelta(0)

        handover = self.df_handover(df)

        return handover, time_shelf

    def change_handover_stationary(self):
        df = self.obj.df_hand_stat

        handover = self.df_handover(df)

        return handover

    def change_time_work(self):
        df = self.obj.df_work
        try:
            df_kitchen = df.drop(df[(df['Категория'] == 'Автомобильный') | (df['Категория'] == 'Велосипедный') | (
                        df['Категория'] == 'Пеший')].index)
            kitchen = pd.to_timedelta(df_kitchen['Итого'].apply(self.change_string)).sum()

        except KeyError:
            kitchen = timedelta(0)

        kitchen = round(kitchen.total_seconds() / 3600, 2)

        return kitchen

    @staticmethod
    def change_productivity(rev: int, tw: float):
        try:
            prod = int(rev / tw)
        except ZeroDivisionError:
            prod = 0
        return prod

    def change_rating(self):
        df_st = self.obj.df_st
        df_prod = self.obj.df_prod
        df_ass = self.obj.df_ass
        df_happy = self.obj.df_happy

        pizza_st = df_st.loc[df_st['Store \n/ \nПиццерия'] == self.obj.name]
        pizza_prod = df_prod.loc[df_prod['Store / Пиццерия'] == self.obj.name]
        pizza_ass = df_ass.loc[df_ass['Store / Пиццерия'] == self.obj.name]
        pizza_happy = df_happy.loc[df_happy['Store / \nПиццерия'] == self.obj.name]
        res_st = pizza_st.iloc[:, -2:].reset_index()
        res_prod = pizza_prod.iloc[:, -4:].reset_index()
        res_ass = pizza_ass.iloc[:, -4:].reset_index()
        res_happy = pizza_happy.iloc[:, -2:].reset_index()
        try:
            res_st1 = float(res_st.iat[0, 1].replace(',', '.'))
            res_st2 = float(res_st.iat[0, 2].replace(',', '.'))
            res_st = round((res_st1 + res_st2) / 2, 2)
        except IndexError:
            res_st = 0
        except AttributeError:
            res_st = 0
        except ValueError:
            res_st = 0
        try:
            res_prod1 = float(res_prod.iat[0, 1].replace(',', '.'))
            res_prod2 = float(res_prod.iat[0, 2].replace(',', '.'))
            res_prod3 = float(res_prod.iat[0, 3].replace(',', '.'))
            res_prod4 = float(res_prod.iat[0, 4].replace(',', '.'))
            res_prod = round((res_prod1 + res_prod2 + res_prod3 + res_prod4) / 4, 2)
        except IndexError:
            res_prod = 0
        except AttributeError:
            res_prod = 0
        except ValueError:
            res_prod = 0
        try:
            res_ass1 = float(res_ass.iat[0, 1].replace(',', '.'))
            res_ass2 = float(res_ass.iat[0, 2].replace(',', '.'))
            res_ass3 = float(res_ass.iat[0, 3].replace(',', '.'))
            res_ass4 = float(res_ass.iat[0, 4].replace(',', '.'))
            res_ass = round((res_ass1 + res_ass2 + res_ass3 + res_ass4) / 4, 2)
        except IndexError:
            res_ass = 0
        except ValueError:
            res_ass = 0
        except AttributeError:
            res_ass = 0
        try:
            res_happy = res_happy.iat[0, 1]
        except IndexError:
            res_happy = 0
        except ValueError:
            res_happy = 0
        except AttributeError:
            res_happy = 0
        return res_st, res_prod, res_ass, res_happy

    def change_product(self):
        product = self.obj.product

        soup = BeautifulSoup(product, 'html.parser')
        finds = soup.find_all("tr", class_="totalForWeek")
        c = 0
        res = ''
        for find in finds:
            f = find.find_all("td", class_="text-right")
            c += 1
            if c == 5:
                res = f
                break
        k = 0
        result = ''
        for i in res:
            if k == 7:
                result = i.text
                break
            k += 1

        return result

    @staticmethod
    def sale(df):
        try:
            total = float(round(df['Сумма'].sum(), 2))
        except KeyError:
            total = 0

        try:
            disc = float(round(df['Amount without discount'].sum(), 2))
        except KeyError:
            disc = 0

        try:
            avg_disc = 100 - (total / disc) * 100
        except ZeroDivisionError:
            avg_disc = 0

        return avg_disc

    def change_sales(self):
        df_sales = self.obj.df_sales
        df_rest = self.obj.df_sales_rest
        df_delivery = self.obj.df_sales_delivery

        avg_disc = self.sale(df_sales)
        avg_disc_rest = self.sale(df_rest)
        avg_disc_delivery = self.sale(df_delivery)

        return avg_disc, avg_disc_rest, avg_disc_delivery
