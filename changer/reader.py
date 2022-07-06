import pandas as pd


class ReadFile:

    def __init__(self, name_rest: str):
        self.name = name_rest

    def open_file(self, order: str, rows: int):
        try:
            df = pd.read_excel(f'./orders/export/{order}_{self.name}.xlsx', skiprows=rows)
        except ValueError:
            df = pd.DataFrame()
        return df

    def open_product(self, order: str):
        pr = ''
        with open(f'./orders/export/{order}_{self.name}.txt', 'rb') as file:
            for line in file:
                pr += line.decode('utf8')
        return pr


class Reader(ReadFile):
    df_rev = None
    df_del = None
    df_stop = None
    df_hand_del = None
    df_hand_stat = None
    product = None
    df_work = None
    df_st = None
    df_prod = None
    df_ass = None
    df_happy = None
    df_sales = None
    df_sales_rest = None
    df_sales_delivery = None

    def read_df(self):
        self.df_rev = self.open_file('revenue', 17)
        self.df_del = self.open_file('del_statistic', 5)
        self.df_stop = self.open_file('being_stop', 5)
        self.df_hand_del = self.open_file('handover-delivery', 6)
        self.df_hand_stat = self.open_file('handover_stationary', 6)
        self.df_work = self.open_file('time_work', 4)
        self.df_sales = self.open_file('sales', 11)
        self.df_sales_rest = self.open_file('sales_rest', 11)
        self.df_sales_delivery = self.open_file('sales_delivery', 11)
        self.df_st = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1824627247',
            on_bad_lines='skip', skiprows=2)
        self.df_prod = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1561264782',
            on_bad_lines='skip', skiprows=1)
        self.df_ass = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1374138695',
            on_bad_lines='skip', skiprows=1)
        self.df_happy = pd.read_csv(
            'https://docs.google.com/spreadsheets/d/1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8/export?format=csv&id=1ua-pStnpfxcnxXbPW2Fsko5HRV2uYBvCJXfGlK18_x8&gid=1919028745',
            on_bad_lines='skip')
        self.product = self.open_product('product')
        