import pytest  # noqa: F401

from src.extract import ler_csv_customers

path = "data/olist_customers_dataset.csv"


def test_carregamento_customers():
    df = ler_csv_customers(path)
    assert not df.empty, "O DataFrame está vazio!"


def test_customer_id_existe_em_orders():  # Deve bater com orders
    pass


def test_customer_unique_id_existe_em_orders():  # Deve bater com orders
    pass


def test_customer_zip_code_prefix_valido():  # Entre 10000 e 99999
    pass


def test_customer_city_nao_nulo():  # Não-nulo
    pass


def test_customer_state_duas_letras():  # Deve ter duas letras (UF)
    pass
