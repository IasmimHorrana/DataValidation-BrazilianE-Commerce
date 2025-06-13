import pytest  # noqa: F401

from src.extract import ler_csv_order_items

path = "data/olist_order_items_dataset.csv"


def test_carregamento_customers():
    df = ler_csv_order_items(path)
    assert not df.empty, "O DataFrame está vazio!"


def test_order_id_existe_em_orders():  # Deve estar presente em orders
    pass


def test_order_item_id_maior_igual_a_uma_vez():  # Deve ser maior que zero
    pass


def test_product_id_nao_nulo():  # Não nulo
    pass


def test_seller_id_nao_nulo():  # Não nulo
    pass


def test_shipping_limit_date_maior_igual_que_purchase_date():
    pass


def test_price_maior_igual_a_zero():  # Deve ser maior que zero
    pass


def test_freight_value_maior_igual_a_zero():  # Deve ser maior que zero
    pass
