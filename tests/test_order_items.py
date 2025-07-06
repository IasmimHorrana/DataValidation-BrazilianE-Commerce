import pandas as pd
from pandas.testing import assert_frame_equal

from src.transform.order_items import (
    converter_order_purchase_timestamp,
    converter_shipping_limit_date,
    filtrar_freight_value_positivo,
    filtrar_order_item_id_valido,
    filtrar_price_positivo,
    filtrar_product_id_valido,
    filtrar_seller_id_valido,
    filtrar_shipping_limit_date_valida,
    merge_order_items_orders,
    transformar_order_items,
)


def test_merge_order_items_orders():
    # DataFrame de items (entrada)
    df_order_items = pd.DataFrame(
        {"order_id": ["o1", "o2", "o4"], "item_id": [1, 2, 3]}
    )

    # DataFrame de pedidos (entrada)
    df_orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "status": ["delivered", "shipped", "canceled"],
        }
    )

    # Resultado esperado
    df_esperado = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o4"],
            "item_id": [1, 2, 3],
            "status": ["delivered", "shipped", pd.NA],
            "_merge": pd.Categorical(
                ["both", "both", "left_only"],
                categories=["left_only", "right_only", "both"],
            ),
        }
    )

    # Conversão explícita de status para aceitar valores nulos
    df_esperado["status"] = df_esperado["status"].astype("object")

    resultado = merge_order_items_orders(df_order_items, df_orders)

    # Seleciona apenas as colunas de interesse e compara
    assert_frame_equal(
        resultado[["order_id", "item_id", "status", "_merge"]].reset_index(
            drop=True
        ),
        df_esperado,
        check_dtype=False,
    )


def test_filtrar_order_item_id_valido():
    df_teste = pd.DataFrame(
        {"order_item_id": [0, 1, 2, -1], "order_id": ["a", "b", "c", "d"]}
    )

    df_esperado = pd.DataFrame(
        {"order_item_id": [1, 2], "order_id": ["b", "c"]}, index=[1, 2]
    )

    resultado = filtrar_order_item_id_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_product_id_valido():
    df_teste = pd.DataFrame(
        {
            "product_id": ["p1", None, "  ", "p2", ""],
            "order_id": ["o1", "o2", "o3", "o4", "o5"],
        }
    )

    df_esperado = pd.DataFrame(
        {"product_id": ["p1", "p2"], "order_id": ["o1", "o4"]}, index=[0, 3]
    )

    resultado = filtrar_product_id_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_seller_id_valido():
    df_teste = pd.DataFrame(
        {
            "seller_id": ["s1", None, "  ", "s2", ""],
            "order_id": ["o1", "o2", "o3", "o4", "o5"],
        }
    )

    df_esperado = pd.DataFrame(
        {"seller_id": ["s1", "s2"], "order_id": ["o1", "o4"]}, index=[0, 3]
    )

    resultado = filtrar_seller_id_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_converter_shipping_limit_date():
    df_teste = pd.DataFrame(
        {
            "shipping_limit_date": [
                "2023-01-01 12:00:00",
                "2023-02-01 15:30:00",
                None,
            ]
        }
    )

    df_esperado = pd.DataFrame(
        {
            "shipping_limit_date": [
                pd.Timestamp("2023-01-01 12:00:00"),
                pd.Timestamp("2023-02-01 15:30:00"),
                pd.NaT,
            ]
        }
    )

    resultado = converter_shipping_limit_date(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_converter_order_purchase_timestamp():
    df_teste = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                "02/10/2017 10:56",
                "invalid_date",
                None,
            ]
        }
    )

    df_esperado = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                pd.Timestamp("2017-10-02 10:56:00"),
                pd.NaT,
                pd.NaT,
            ]
        }
    )

    resultado = converter_order_purchase_timestamp(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_shipping_limit_date_valida():
    df_teste = pd.DataFrame(
        {
            "shipping_limit_date": [
                pd.Timestamp("2018-08-10 12:00"),
                pd.Timestamp("2018-08-09 12:00"),
                pd.Timestamp("2018-08-11 12:00"),
            ],
            "order_purchase_timestamp": [
                pd.Timestamp("2018-08-10 11:00"),
                pd.Timestamp("2018-08-10 12:00"),
                pd.Timestamp("2018-08-11 12:00"),
            ],
        }
    )

    df_esperado = pd.DataFrame(
        {
            "shipping_limit_date": [
                pd.Timestamp("2018-08-10 12:00"),
                pd.Timestamp("2018-08-11 12:00"),
            ],
            "order_purchase_timestamp": [
                pd.Timestamp("2018-08-10 11:00"),
                pd.Timestamp("2018-08-11 12:00"),
            ],
        },
        index=[0, 2],
    )

    resultado = filtrar_shipping_limit_date_valida(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_price_positivo():
    df_teste = pd.DataFrame({"price": [10.5, 0, -3.0, 5.0]})

    df_esperado = pd.DataFrame({"price": [10.5, 5.0]}, index=[0, 3])

    resultado = filtrar_price_positivo(df_teste)

    assert_frame_equal(resultado, df_esperado)


def test_filtrar_freight_value_positivo():
    df_teste = pd.DataFrame({"freight_value": [10.0, 0.0, -5.0, 3.5]})

    df_esperado = pd.DataFrame({"freight_value": [10.0, 3.5]}, index=[0, 3])

    resultado = filtrar_freight_value_positivo(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_transformar_order_items():
    df_order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "order_item_id": [1, 0, 2, 3],
            "product_id": ["p1", "", None, "p4"],
            "seller_id": ["s1", "s2", "", "s4"],
            "shipping_limit_date": [
                "2023-01-10",
                "2023-01-11",
                "2023-01-09",
                "2023-01-12",
            ],
            "order_purchase_timestamp": [
                "2023-01-05",
                "2023-01-07",
                "2023-01-08",
                "2023-01-06",
            ],
            "price": [10.5, -5.0, 20.0, 15.0],
            "freight_value": [2.0, 0.0, -1.0, 5.0],
        }
    )

    df_orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "some_other_column": [100, 200, 300],
        }
    )

    # Convertendo datas para datetime para evitar problemas na comparação
    df_order_items["shipping_limit_date"] = pd.to_datetime(
        df_order_items["shipping_limit_date"]
    )
    df_order_items["order_purchase_timestamp"] = pd.to_datetime(
        df_order_items["order_purchase_timestamp"]
    )

    resultado = transformar_order_items(df_order_items, df_orders)

    # Verificações:
    # - order_item_id >=1
    assert (resultado["order_item_id"] >= 1).all()
    # - product_id não vazio ou None
    assert resultado["product_id"].notna().all()
    assert (resultado["product_id"].str.strip() != "").all()
    # - seller_id não vazio
    assert resultado["seller_id"].notna().all()
    assert (resultado["seller_id"].str.strip() != "").all()
    # - shipping_limit_date >= order_purchase_timestamp
    assert (
        resultado["shipping_limit_date"]
        >= resultado["order_purchase_timestamp"]
    ).all()
    # - price positivo
    assert (resultado["price"] > 0).all()
    # - freight_value positivo
    assert (resultado["freight_value"] > 0).all()
    # - order_id existe em orders
    assert resultado["order_id"].isin(df_orders["order_id"]).all()
