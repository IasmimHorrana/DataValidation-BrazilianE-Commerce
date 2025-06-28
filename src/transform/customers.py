def filtrar_customer_id(df):
    """
    Filtra registros com customer_id de exatamente 32 caracteres.
    Isso garante que o ID do cliente tenha o formato correto esperado,
    evitando registros inválidos ou corrompidos.
    """
    return df[df["customer_id"].str.len() == 32]


def filtrar_customer_unique_id(df):
    """
    Filtra registros com customer_unique_id de exatamente 32 caracteres.
    O unique_id deve ter o tamanho correto para assegurar a unicidade
    e integridade dos dados.
    """
    return df[df["customer_unique_id"].str.len() == 32]


def filtrar_customer_zip_code_valido(df):
    """
    Filtra códigos postais que estejam dentro de um intervalo plausível
    (1000 a 99999).
    """
    return df[
        (df["customer_zip_code_prefix"] >= 1000)
        & (df["customer_zip_code_prefix"] <= 99999)
    ]


def filtrar_customer_city_valido(df):
    """
    Mantém apenas cidades válidas, não nulas e com nome mínimo de 3 caracteres.
    Isso evita registros com cidades ausentes ou nomes inválidos.
    """
    return df[
        (df["customer_city"].notnull()) & (df["customer_city"].str.len() >= 3)
    ]


def filtrar_customer_state_duas_letras(df):
    """
    Valida que o estado está em formato abreviado de 2 letras (sigla).
    Garante padronização e evita dados incompletos ou incorretos nesse campo.
    """
    return df[df["customer_state"].str.len() == 2]


def transformar_customers(df):
    """
    Aplica todas as transformações e filtros no DataFrame de customers.
    Retorna o DataFrame filtrado e limpo conforme as regras definidas.
    """
    df = filtrar_customer_id(df)
    df = filtrar_customer_unique_id(df)
    df = filtrar_customer_zip_code_valido(df)
    df = filtrar_customer_city_valido(df)
    df = filtrar_customer_state_duas_letras(df)
    return df
