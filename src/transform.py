import pandas as pd


def transformar_customers(df):
    # Mantém apenas os registros com customer_id e
    # customer_unique_id com exatamente 32 caracteres
    df = df[
        (df["customer_id"].str.len() == 32)
        & (df["customer_unique_id"].str.len() == 32)
    ]
    # Inteiro entre 1000 a 99999 (Filtrar prefixos fora do intervalo)
    df = df[
        (df["customer_zip_code_prefix"] >= 1000)
        & (df["customer_zip_code_prefix"] <= 99999)
    ]
    # Não pode ser Nulo e o minimo de 3 caracters
    df = df[
        (df["customer_city"].notnull()) & (df["customer_city"].str.len() >= 3)
    ]
    # Sigla com exatamente 2 letras
    df = df[df["customer_state"].str.len() == 2]

    return df


def transformar_orders(df_orders, df_customers):
    # Remover duplicatas e validar tamanho do order_id
    df_orders = df_orders.drop_duplicates(subset=["order_id"], keep="first")
    df_orders = df_orders[df_orders["order_id"].str.len() == 32]

    # Verificar se customer_id do orders existe no customers
    df_merge = pd.merge(
        df_orders, df_customers, on="customer_id", how="left", indicator=True
    )

    # Filtrar os pedidos com customer_id inválido
    pedidos_invalidos = df_merge[df_merge["_merge"] == "left_only"]

    # Remover os inválidos e seguir com os válidos
    pedidos_validos = df_merge[df_merge["_merge"] == "both"].drop(
        columns=["_merge"]
    )

    # Filtrar valores específicos em order_status
    pedidos_validos = pedidos_validos[
        pedidos_validos["order_status"].isin(
            [
                "delivered",
                "invoiced",
                "shipped",
                "processing",
                "unavailable",
                "approved",
                "canceled",
                "created",
            ]
        )
    ]

    # Remover registros com order_purchase_timestamp nulo
    pedidos_validos = pedidos_validos[
        pedidos_validos["order_purchase_timestamp"].notna()
    ]

    # Verificar se data estimada >= data da compra
    pedidos_validos["data_ok"] = pedidos_validos[
        "order_estimated_delivery_date"
    ].notna() & (
        pedidos_validos["order_estimated_delivery_date"]
        >= pedidos_validos["order_purchase_timestamp"]
    )

    # Validar se order_approved_at está coerente com o status
    status_que_exigem_aprovacao = [
        "approved",
        "shipped",
        "delivered",
        "invoiced",
        "processing",
    ]

    pedidos_validos["aprovacao_valida"] = (
        ~pedidos_validos["order_status"].isin(status_que_exigem_aprovacao)
    ) | pedidos_validos["order_approved_at"].notna()

    return pedidos_validos, pedidos_invalidos


def transformar_order_items(df_order_items, df_orders):
    # Merge para validar se order_id existe
    df_merge = pd.merge(
        df_order_items, df_orders, on="order_id", how="left", indicator=True
    )

    # order_item_id >= 1
    df_merge = df_merge[df_merge["order_item_id"] >= 1]

    # product_id não nulo e não vazio
    df_merge = df_merge[
        df_merge["product_id"].notna()
        & (df_merge["product_id"].str.strip() != "")
    ]

    # seller_id não nulo e não vazio
    df_merge = df_merge[
        df_merge["seller_id"].notna()
        & (df_merge["seller_id"].str.strip() != "")
    ]

    # Garantir que as datas estão como datetime
    df_merge["shipping_limit_date"] = pd.to_datetime(
        df_merge["shipping_limit_date"]
    )
    df_merge["order_purchase_timestamp"] = pd.to_datetime(
        df_merge["order_purchase_timestamp"]
    )

    # shipping_limit_date >= order_purchase_timestamp
    df_merge = df_merge[
        df_merge["shipping_limit_date"] >= df_merge["order_purchase_timestamp"]
    ]

    # price > 0
    df_merge = df_merge[df_merge["price"] > 0]

    # freight_value > 0
    df_merge = df_merge[df_merge["freight_value"] > 0]

    return df_merge
