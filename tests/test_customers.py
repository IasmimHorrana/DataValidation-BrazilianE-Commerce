import pandas as pd
import pytest  # noqa: F401
from pandas.testing import assert_frame_equal

from src.transform.customers import (
    filtrar_customer_id,
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
    pass


def test_filtrar_customer_zip_code_valido():
    pass


def test_filtrar_customer_city_valido():
    pass


def test_filtrar_customer_state_duas_letras():
    pass
