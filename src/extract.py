import pandas as pd

from src.logger_config import logger


def ler_csv_customers(path: str) -> pd.DataFrame:
    logger.info(f"Iniciando leitura do arquivo: {path}")
    try:
        df = pd.read_csv(path, sep=";")
        logger.success(f"Leitura concluída com sucesso. Linhas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler {path}: {e}")
        raise


def ler_csv_orders(path: str) -> pd.DataFrame:
    logger.info(f"Iniciando leitura do arquivo: {path}")
    try:
        df = pd.read_csv(path, sep=";")
        logger.success(f"Leitura concluída com sucesso. Linhas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler {path}: {e}")
        raise


def ler_csv_order_items(path: str) -> pd.DataFrame:
    logger.info(f"Iniciando leitura do arquivo: {path}")
    try:
        df = pd.read_csv(path, sep=";")
        logger.success(f"Leitura concluída com sucesso. Linhas: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Erro ao ler {path}: {e}")
        raise
