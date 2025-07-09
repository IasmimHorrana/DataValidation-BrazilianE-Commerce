import pandas as pd

from src.decorators.log_extraction import log_csv_extraction


@log_csv_extraction("logs/extract/extract_customers.log")
def ler_csv_customers(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


@log_csv_extraction("logs/extract/extract_orders.log")
def ler_csv_orders(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


@log_csv_extraction("logs/extract/extract_order_items.log")
def ler_csv_order_items(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")
