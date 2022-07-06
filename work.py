from exporter.exporter import save_orders
from changer.application import change_orders


def worker(group):
    save_orders(group)
    change_orders(group)

