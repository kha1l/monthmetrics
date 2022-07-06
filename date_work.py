from datetime import date, timedelta


class DataWork:

    def __init__(self, date_end=None):
        self.date_end = date_end

    @staticmethod
    def get_month(dt):
        month = int(dt.strftime('%m'))
        year = int(dt.strftime('%Y'))
        month_begin = date(year, month, 1)
        return month_begin

    def set_date(self):
        if self.date_end is None:
            self.date_end = date.today() - timedelta(days=1)
            return self.date_end
        else:
            return self.date_end
