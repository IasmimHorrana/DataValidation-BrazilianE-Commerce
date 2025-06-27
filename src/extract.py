import pandas as pd

# Esse modulo contém funções para ler CSV com pandas.


def ler_csv_customers(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


def ler_csv_orders(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


def ler_csv_order_items(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")
