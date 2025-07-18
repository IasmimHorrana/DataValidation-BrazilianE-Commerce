import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.types import BigInteger, Boolean, DateTime, Float

from src.extract import ler_csv_customers, ler_csv_order_items, ler_csv_orders
from src.transform import (
    transformar_customers,
    transformar_order_items,
    transformar_orders,
)


def carregar_variaveis_ambiente():
    load_dotenv()
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME"),
    }


def criar_engine_postgres(config):
    url = (
        "postgresql+psycopg2://"
        f"{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )
    return create_engine(url)


def executar_etl(engine):
    print("Iniciando pipeline de ETL...")

    # 1. Extração
    df_customers = ler_csv_customers("data/olist_customers_dataset.csv")
    df_orders = ler_csv_orders("data/olist_orders_dataset.csv")
    df_order_items = ler_csv_order_items("data/olist_order_items_dataset.csv")

    # 2. Transformação
    df_customers_limpo = transformar_customers(df_customers)
    df_orders_limpo, df_orders_invalidos = transformar_orders(
        df_orders, df_customers_limpo
    )
    df_order_items_limpo = transformar_order_items(
        df_order_items, df_orders_limpo
    )

    # 3. Salvar CSVs transformados
    os.makedirs("data/transformados", exist_ok=True)
    df_customers_limpo.to_csv(
        "data/transformados/olist_customers.csv", index=False
    )
    df_orders_limpo.to_csv("data/transformados/olist_orders.csv", index=False)
    df_orders_invalidos.to_csv(
        "data/transformados/olist_orders_invalidos.csv", index=False
    )
    df_order_items_limpo.to_csv(
        "data/transformados/olist_order_items.csv", index=False
    )

    # 4. Carga no banco de dados
    print("Salvando os dados no banco PostgreSQL...")

    df_customers_limpo.to_sql(
        "customers", engine, if_exists="replace", index=False
    )

    df_orders_limpo.to_sql(
        "orders",
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "order_purchase_timestamp": DateTime(),
            "order_approved_at": DateTime(),
            "order_delivered_carrier_date": DateTime(),
            "order_delivered_customer_date": DateTime(),
            "order_estimated_delivery_date": DateTime(),
        },
    )

    df_orders_invalidos.to_sql(
        "orders_invalidos",
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "order_purchase_timestamp": DateTime(),
            "order_approved_at": DateTime(),
            "order_delivered_carrier_date": DateTime(),
            "order_delivered_customer_date": DateTime(),
            "order_estimated_delivery_date": DateTime(),
        },
    )

    df_order_items_limpo.to_sql(
        "order_items",
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "order_item_id": BigInteger(),
            "shipping_limit_date": DateTime(),
            "order_purchase_timestamp": DateTime(),
            "order_approved_at": DateTime(),
            "order_delivered_carrier_date": DateTime(),
            "order_delivered_customer_date": DateTime(),
            "order_estimated_delivery_date": DateTime(),
            "price": Float(),
            "freight_value": Float(),
            "data_ok": Boolean(),
            "aprovacao_valida": Boolean(),
            "customer_zip_code_prefix": BigInteger(),
        },
    )

    print("Pipeline concluído com sucesso!")


def main():
    config_db = carregar_variaveis_ambiente()
    engine = criar_engine_postgres(config_db)
    executar_etl(engine)


if __name__ == "__main__":
    main()
