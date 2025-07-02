import pandas as pd
import pytest

from src.extract import ler_csv_customers, ler_csv_order_items, ler_csv_orders

# Dados de exemplo em memória
CSV_CONTENT = "coluna1;coluna2\nvalor1;valor2\nvalor3;valor4"


@pytest.fixture
def arquivo_csv_temporario(tmp_path):
    """Cria um arquivo CSV temporário para os testes."""
    caminho = tmp_path / "arquivo.csv"
    caminho.write_text(CSV_CONTENT)
    return str(caminho)


def test_ler_csv_customers(arquivo_csv_temporario):
    df = ler_csv_customers(arquivo_csv_temporario)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["coluna1", "coluna2"]


def test_ler_csv_orders(arquivo_csv_temporario):
    df = ler_csv_orders(arquivo_csv_temporario)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["coluna1", "coluna2"]


def test_ler_csv_order_items(arquivo_csv_temporario):
    df = ler_csv_order_items(arquivo_csv_temporario)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["coluna1", "coluna2"]
