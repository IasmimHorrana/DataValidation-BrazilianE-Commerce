import pytest  # noqa: F401

from src.extract import ler_csv_orders

path = "data/olist_orders_dataset.csv"


def test_carregamento_customers():
    df = ler_csv_orders(path)
    assert not df.empty, "O DataFrame está vazio!"


def test_order_id_deve_ser_unico():  # Deve ser unico e não nulo
    pass


def customer_id_existe_em_customers():  # Deve estar presente
    pass


# delivered, invoiced, shipped, processing, unavailable,
# approved, canceled, created
def order_status_valido():
    pass


def order_purchase_timestamp_nao_nulo():  # Não nulo
    pass


# Pode ser nulo se não aprovado
def test_order_approved_at_nao_nulo_quando_status_aprovado():
    pass


def order_delivered_carrier_date_pode_ser_nulo():  # Pode ser nulo
    pass


def order_delivered_customer_date_pode_ser_nulo():  # Pode ser nulo
    pass


# Não deve ser nulo > purchase_timestamp
def order_estimated_delivery_date_nao_nulo():
    pass
