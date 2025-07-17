import pandas as pd
from sqlalchemy import text

from utils.conexao import engine


def carregar_query(caminho_sql, **params):
    """
    Executa uma query SQL a partir de um arquivo e retorna
    o resultado em um DataFrame.

    Parâmetros:
    - caminho_sql (str): caminho para o arquivo .sql que contém a query.
    - **params: parâmetros nomeados para substituir na query (ex: filtros).

    Retorna:
    - pd.DataFrame: resultado da consulta SQL.
    """
    # Abre o arquivo SQL e lê o conteúdo
    with open(caminho_sql, "r") as arquivo:
        query = text(arquivo.read())  # Cria um objeto para parametrização
    # Abre conexão com o banco usando a engine e executa a query
    with engine.connect() as conexao:
        df = pd.read_sql_query(query, conexao, params=params)
    return df
