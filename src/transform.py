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
