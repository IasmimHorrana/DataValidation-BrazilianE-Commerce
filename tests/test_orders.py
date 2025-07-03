import pandas as pd
from pandas.testing import assert_frame_equal

from src.transform.orders import (
    converter_order_purchase_timestamp,
    customer_id_existe_em_customers,
    filtrar_order_id_deve_ser_unico,
    filtrar_order_status_valido,
    filtrar_orders_validos,
    remove_registros_com_order_purchase_timestamp_nulo,
    transformar_orders,
    verifica_aprovacao_status,
    verifica_data_estimada,
)


def test_filtrar_order_id_deve_ser_unico():
    df_teste = pd.DataFrame(
        {
            "order_id": [
                "a" * 32,  # válido
                "a" * 32,  # duplicado
                "b" * 32,  # válido
                "c" * 30,  # inválido
                "d" * 33,  # inválido
            ],
            "valor": [1, 2, 3, 4, 5],
        }
    )

    df_esperado = pd.DataFrame(
        {"order_id": ["a" * 32, "b" * 32], "valor": [1, 3]}, index=[0, 2]
    )

    resultado = filtrar_order_id_deve_ser_unico(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_customer_id_existe_em_customers():
    df_orders = pd.DataFrame(
        {"order_id": ["o1", "o2", "o3"], "customer_id": ["c1", "c2", "c4"]}
    )

    df_customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
            "customer_nome": ["Ana", "Bruno", "Carlos"],
        }
    )

    df_esperado = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "customer_id": ["c1", "c2", "c4"],
            "customer_nome": ["Ana", "Bruno", None],
            "_merge": ["both", "both", "left_only"],
        }
    )

    resultado = customer_id_existe_em_customers(df_orders, df_customers)

    # Converte _merge para string para facilitar comparação
    resultado["_merge"] = resultado["_merge"].astype(str)

    assert_frame_equal(
        resultado[
            ["order_id", "customer_id", "customer_nome", "_merge"]
        ].reset_index(drop=True),
        df_esperado,
        check_dtype=False,
    )


def test_filtrar_orders_validos():
    # Arrange: cria o df de entrada simulando o resultado de um merge
    df_merge = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c2", "c3", "c4"],
            "_merge": ["both", "left_only", "both", "left_only"],
        }
    )

    # Esperado: apenas registros com _merge == 'both', sem a coluna _merge
    df_validos = pd.DataFrame(
        {"order_id": ["o1", "o3"], "customer_id": ["c1", "c3"]}, index=[0, 2]
    )  # mantém índice original

    # Esperado: registros com _merge == 'left_only', mantendo _merge
    df_invalidos = pd.DataFrame(
        {
            "order_id": ["o2", "o4"],
            "customer_id": ["c2", "c4"],
            "_merge": ["left_only", "left_only"],
        },
        index=[1, 3],
    )

    # Act
    validos, invalidos = filtrar_orders_validos(df_merge)

    # Assert
    assert_frame_equal(validos, df_validos)
    assert_frame_equal(invalidos, df_invalidos)


def test_filtrar_order_status_valido():
    # Arrange: cria um DataFrame com alguns status válidos e inválidos
    df_teste = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "order_status": ["delivered", "unknown", "shipped", "erro"],
        }
    )

    df_esperado = pd.DataFrame(
        {"order_id": ["o1", "o3"], "order_status": ["delivered", "shipped"]},
        index=[0, 2],
    )

    resultado = filtrar_order_status_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_converter_order_purchase_timestamp():
    df_teste = pd.DataFrame(
        {"order_purchase_timestamp": ["02/10/2017 10:56", "invalid date"]}
    )

    df_esperado = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                pd.Timestamp("2017-10-02 10:56:00"),
                pd.NaT,
            ]
        }
    )

    resultado = converter_order_purchase_timestamp(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_remove_registros_com_order_purchase_timestamp_nulo():
    df_teste = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                pd.Timestamp("2017-10-02 10:56:00"),
                pd.NaT,
            ]
        }
    )

    df_esperado = pd.DataFrame(
        {"order_purchase_timestamp": [pd.Timestamp("2017-10-02 10:56:00")]},
        index=[0],
    )

    resultado = remove_registros_com_order_purchase_timestamp_nulo(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_verifica_data_estimada():
    df_teste = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                pd.Timestamp("2023-01-01"),
                pd.Timestamp("2023-01-05"),
                pd.Timestamp("2023-01-10"),
                pd.Timestamp("2023-01-15"),
            ],
            "order_estimated_delivery_date": [
                pd.Timestamp("2023-01-03"),  # válido (posterior)
                pd.NaT,  # inválido (nulo)
                pd.Timestamp("2023-01-05"),  # inválido (anterior)
                pd.Timestamp("2023-01-15"),  # válido (igual)
            ],
        }
    )

    df_esperado = df_teste.copy()
    df_esperado["data_ok"] = [True, False, False, True]

    resultado = verifica_data_estimada(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_verifica_aprovacao_status():
    df_teste = pd.DataFrame(
        {
            "order_status": [
                "approved",  # exige aprovação, mas está com NaT → False
                "shipped",  # exige aprovação, com valor → True
                "created",  # NÃO exige aprovação → True
                "delivered",  # exige aprovação, com valor → True
                "processing",  # exige aprovação, mas está com NaT → False
            ],
            "order_approved_at": [
                pd.NaT,
                pd.Timestamp("2023-01-05"),
                pd.NaT,
                pd.Timestamp("2023-01-07"),
                pd.NaT,
            ],
        }
    )

    df_esperado = df_teste.copy()
    df_esperado["aprovacao_valida"] = [False, True, True, True, False]

    resultado = verifica_aprovacao_status(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_transformar_orders():
    # Dados de entrada
    df_orders = pd.DataFrame(
        {
            "order_id": [
                "o" * 32,
                "x" * 32,
                "dup" * 10 + "1",
                "z" * 32,
            ],  # 3 válidos, 1 duplicado
            "customer_id": [
                "c1",
                "c2",
                "c1",
                "c3",
            ],  # c3 não está em df_customers
            "order_status": ["delivered", "created", "shipped", "approved"],
            "order_purchase_timestamp": [
                "02/10/2017 10:56",
                "08/08/2018 08:38",
                "01/01/2018 08:00",
                None,
            ],
            "order_estimated_delivery_date": [
                "05/10/2017 10:56",
                "10/08/2018 08:38",
                "01/01/2018 10:00",
                "05/01/2018 09:00",
            ],
            "order_approved_at": [pd.NaT, pd.NaT, "01/01/2018 09:00", None],
        }
    )

    df_customers = pd.DataFrame(
        {"customer_id": ["c1", "c2"], "customer_nome": ["Ana", "Bruno"]}
    )

    # Conversão manual esperada para timestamps
    df_orders["order_purchase_timestamp"] = pd.to_datetime(
        df_orders["order_purchase_timestamp"],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )
    df_orders["order_estimated_delivery_date"] = pd.to_datetime(
        df_orders["order_estimated_delivery_date"],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )
    df_orders["order_approved_at"] = pd.to_datetime(
        df_orders["order_approved_at"],
        format="%d/%m/%Y %H:%M",
        errors="coerce",
    )

    # Chamada da função
    pedidos_validos, pedidos_invalidos = transformar_orders(
        df_orders, df_customers
    )

    # Verificações básicas (você pode ajustar conforme suas regras)
    assert not pedidos_validos.empty
    assert "data_ok" in pedidos_validos.columns
    assert "aprovacao_valida" in pedidos_validos.columns

    # Checagem se o pedido com customer_id inválido foi para inválidos
    assert "c3" in pedidos_invalidos["customer_id"].values

    # Checagem se todos os pedidos válidos têm order_id de 32 caracteres
    assert all(pedidos_validos["order_id"].str.len() == 32)
