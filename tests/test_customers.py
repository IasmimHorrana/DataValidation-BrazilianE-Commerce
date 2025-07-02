import pandas as pd
from pandas.testing import assert_frame_equal

from src.transform.customers import (
    filtrar_customer_city_valido,
    filtrar_customer_id,
    filtrar_customer_state_duas_letras,
    filtrar_customer_unique_id,
    filtrar_customer_zip_code_valido,
    transformar_customers,
)


def test_filtrar_customer_id():
    # Arrange: DataFrame de teste com alguns valores válidos e inválidos
    df_teste = pd.DataFrame(
        {"customer_id": ["a" * 32, "b" * 30, "c" * 32], "valor": [1, 2, 3]}
    )

    # Esperado: apenas as linhas com customer_id de 32 caracteres
    df_esperado = pd.DataFrame(
        {"customer_id": ["a" * 32, "c" * 32], "valor": [1, 3]}, index=[0, 2]
    )  # mantém os índices originais se a função não resetar o índice

    # Act: executa a função
    resultado = filtrar_customer_id(df_teste)

    # Assert: compara com o DataFrame esperado
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_customer_unique_id():
    df_teste = pd.DataFrame(
        {
            "customer_unique_id": ["a" * 32, "b" * 30, "c" * 32],
            "valor": [1, 2, 3],
        }
    )

    df_esperado = pd.DataFrame(
        {"customer_unique_id": ["a" * 32, "c" * 32], "valor": [1, 3]},
        index=[0, 2],
    )

    resultado = filtrar_customer_unique_id(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_customer_zip_code_valido():
    df_teste = pd.DataFrame(
        {"customer_zip_code_prefix": [123, 1234, 12345], "valor": [1, 2, 3]}
    )
    df_esperado = pd.DataFrame(
        {"customer_zip_code_prefix": [1234, 12345], "valor": [2, 3]},
        index=[1, 2],
    )
    resultado = filtrar_customer_zip_code_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_customer_city_valido():
    df_teste = pd.DataFrame(
        {"customer_city": ["", "Rio", "BA"], "valor": [1, 2, 3]}
    )
    df_esperado = pd.DataFrame(
        {"customer_city": ["Rio"], "valor": [2]}, index=[1]
    )
    resultado = filtrar_customer_city_valido(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_filtrar_customer_state_duas_letras():
    df_teste = pd.DataFrame(
        {
            "customer_state": ["", "BA", None, "SP", "RJS"],
            "valor": [1, 2, 3, 4, 5],
        }
    )
    df_esperado = pd.DataFrame(
        {"customer_state": ["BA", "SP"], "valor": [2, 4]}, index=[1, 3]
    )
    resultado = filtrar_customer_state_duas_letras(df_teste)
    assert_frame_equal(resultado, df_esperado)


def test_transformar_customers():
    df_teste = pd.DataFrame(
        {
            "customer_id": ["a" * 32, "b" * 30],
            "customer_unique_id": ["u" * 32, "u" * 30],
            "customer_zip_code_prefix": [1000, 999],
            "customer_city": ["São Paulo", ""],
            "customer_state": ["SP", "SPO"],
            "valor": [1, 2],
        }
    )

    df_esperado = pd.DataFrame(
        {
            "customer_id": ["a" * 32],
            "customer_unique_id": ["u" * 32],
            "customer_zip_code_prefix": [1000],
            "customer_city": ["São Paulo"],
            "customer_state": ["SP"],
            "valor": [1],
        },
        index=[0],
    )

    resultado = transformar_customers(df_teste)
    assert_frame_equal(resultado, df_esperado)
