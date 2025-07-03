import pandas as pd


def filtrar_order_id_deve_ser_unico(df_orders):
    """
    Remove duplicatas com base em 'order_id' e filtra registros
    cujo 'order_id' possui exatamente 32 caracteres.
    """
    df_orders = df_orders.drop_duplicates(subset=["order_id"], keep="first")
    df_orders = df_orders[df_orders["order_id"].str.len() == 32]
    return df_orders


def customer_id_existe_em_customers(df_orders, df_customers):
    """
    Realiza merge para verificar se 'customer_id' em pedidos existe
    no DataFrame de clientes.
    """
    df_merge = pd.merge(
        df_orders, df_customers, on="customer_id", how="left", indicator=True
    )
    return df_merge


def filtrar_orders_validos(df_merge):
    """
    Separa pedidos com 'customer_id' inválido e retorna DataFrames de
    pedidos válidos e inválidos.
    """
    pedidos_invalidos = df_merge[df_merge["_merge"] == "left_only"]
    pedidos_validos = df_merge[df_merge["_merge"] == "both"].drop(
        columns=["_merge"]
    )
    return pedidos_validos, pedidos_invalidos


def filtrar_order_status_valido(pedidos_validos):
    """
    Filtra pedidos mantendo apenas os que possuem 'order_status'
    em uma lista válida.
    """
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
    return pedidos_validos


def converter_order_purchase_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte a coluna 'order_purchase_timestamp' para datetime.
    """
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce", dayfirst=True
    )
    return df


def remove_registros_com_order_purchase_timestamp_nulo(pedidos_validos):
    """
    Remove registros com 'order_purchase_timestamp' nulo.
    """
    pedidos_validos = pedidos_validos[
        pedidos_validos["order_purchase_timestamp"].notna()
    ]
    return pedidos_validos


def verifica_data_estimada(pedidos_validos):
    """
    Cria coluna 'data_ok' que valida se 'order_estimated_delivery_date'
    não é nulo e é maior ou igual a 'order_purchase_timestamp'.
    """
    pedidos_validos["data_ok"] = pedidos_validos[
        "order_estimated_delivery_date"
    ].notna() & (
        pedidos_validos["order_estimated_delivery_date"]
        >= pedidos_validos["order_purchase_timestamp"]
    )
    return pedidos_validos


def verifica_aprovacao_status(pedidos_validos):
    """
    Cria coluna 'aprovacao_valida' que valida se o campo 'order_approved_at'
    está presente nos pedidos cujo status exige aprovação.
    """
    status_que_exigem_aprovacao = [
        "approved",
        "shipped",
        "delivered",
        "invoiced",
        "processing",
    ]
    pedidos_validos["aprovacao_valida"] = (
        ~pedidos_validos["order_status"].isin(status_que_exigem_aprovacao)
        | pedidos_validos["order_approved_at"].notna()
    )
    return pedidos_validos


def transformar_orders(df_orders, df_customers):
    """
    Aplica todas as transformações e validações ao DataFrame de pedidos,
    utilizando dados de clientes para consistência de relacionamento.
    Retorna dois DataFrames: pedidos válidos e pedidos inválidos.
    """
    df_orders = filtrar_order_id_deve_ser_unico(df_orders)
    df_orders = converter_order_purchase_timestamp(df_orders)
    df_merge = customer_id_existe_em_customers(df_orders, df_customers)
    pedidos_validos, pedidos_invalidos = filtrar_orders_validos(df_merge)
    pedidos_validos = filtrar_order_status_valido(pedidos_validos)
    pedidos_validos = remove_registros_com_order_purchase_timestamp_nulo(
        pedidos_validos
    )
    pedidos_validos = verifica_data_estimada(pedidos_validos)
    pedidos_validos = verifica_aprovacao_status(pedidos_validos)
    return pedidos_validos, pedidos_invalidos
