import pandas as pd

from src.decorators.logging_utils import log_dataset


@log_dataset("order_items")
def merge_order_items_orders(df_order_items, df_orders):
    """
    Realiza merge para validar se os order_id em order_items existem em orders.
    """
    df_merge = pd.merge(
        df_order_items, df_orders, on="order_id", how="left", indicator=True
    )
    return df_merge


@log_dataset("order_items")
def filtrar_order_item_id_valido(df_merge):
    """
    Filtra registros onde order_item_id é maior ou igual a 1.
    """
    return df_merge[df_merge["order_item_id"] >= 1]


@log_dataset("order_items")
def filtrar_product_id_valido(df_merge):
    """
    Remove registros com product_id nulo ou string vazia.
    """
    return df_merge[
        df_merge["product_id"].notna()
        & (df_merge["product_id"].str.strip() != "")
    ]


@log_dataset("order_items")
def filtrar_seller_id_valido(df_merge):
    """
    Remove registros com seller_id nulo ou string vazia.
    """
    return df_merge[
        df_merge["seller_id"].notna()
        & (df_merge["seller_id"].str.strip() != "")
    ]


@log_dataset("order_items")
def converter_shipping_limit_date(df_merge):
    """
    Converte a coluna shipping_limit_date para datetime.
    """
    df_merge["shipping_limit_date"] = pd.to_datetime(
        df_merge["shipping_limit_date"]
    )
    return df_merge


@log_dataset("order_items")
def converter_order_purchase_timestamp(df_merge):
    """
    Converte a coluna order_purchase_timestamp para datetime,
    considerando formato dia/mês/ano.
    """
    df_merge["order_purchase_timestamp"] = pd.to_datetime(
        df_merge["order_purchase_timestamp"], dayfirst=True, errors="coerce"
    )
    return df_merge


@log_dataset("order_items")
def filtrar_shipping_limit_date_valida(df_merge):
    """
    Filtra registros onde shipping_limit_date é maior ou igual
    a order_purchase_timestamp.
    """
    return df_merge[
        df_merge["shipping_limit_date"] >= df_merge["order_purchase_timestamp"]
    ]


@log_dataset("order_items")
def filtrar_price_positivo(df_merge):
    """
    Remove registros com price menor ou igual a zero.
    """
    return df_merge[df_merge["price"] > 0]


@log_dataset("order_items")
def filtrar_freight_value_positivo(df_merge):
    """
    Remove registros com freight_value menor ou igual a zero.
    """
    return df_merge[df_merge["freight_value"] > 0]


@log_dataset("order_items")
def transformar_order_items(df_order_items, df_orders):
    """
    Função principal que aplica todas as transformações de limpeza e validação
    """
    df_merge = merge_order_items_orders(df_order_items, df_orders)
    # Filtra somente linhas com order_id presente em df_orders
    df_merge = df_merge[df_merge["_merge"] == "both"].copy()
    df_merge = filtrar_order_item_id_valido(df_merge)
    df_merge = filtrar_product_id_valido(df_merge)
    df_merge = filtrar_seller_id_valido(df_merge)
    df_merge = converter_shipping_limit_date(df_merge)
    df_merge = converter_order_purchase_timestamp(df_merge)
    df_merge = filtrar_shipping_limit_date_valida(df_merge)
    df_merge = filtrar_price_positivo(df_merge)
    df_merge = filtrar_freight_value_positivo(df_merge)

    return df_merge.drop(columns=["_merge"])
