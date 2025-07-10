"""
logging_utils.py

Este módulo centraliza a configuração de logs do projeto,
utilizando a biblioteca Loguru. Ele define:

- Logs no terminal (coloridos e informativos)
- Logs salvos em arquivos separados por dataset
- Um decorator (@log_dataset) que pode ser usado em funções para registrar:
    - Quando a função foi chamada
    - Se ela executou com sucesso
    - Se ela gerou erro

Ideal para rastrear a execução de funções de transformação e extração de dados.
"""

import os  # Para criar diretórios, se necessário
from functools import wraps  # Para preservar metadata ao criar decorators
from sys import stderr  # Para mostrar logs no terminal

from loguru import logger  # Biblioteca usada para logging elegante

# Garante que a pasta 'logs' exista
os.makedirs("logs", exist_ok=True)

# Remove qualquer configuração de log anterior para evitar duplicação
logger.remove()

# Adiciona saída de log no terminal (stdout), colorido e com timestamp
logger.add(
    sink=stderr,  # Envia para o terminal
    format="{time:YYYY-MM-DD HH:mm:ss} <level>{level}</level> "
    "<cyan>{message}</cyan>",
    level="INFO",  # Exibe logs de nível INFO ou superior
)

# Add log em arquivo apenas para funções relacionadas ao dataset: 'customers'
logger.add(
    "logs/customers.log",
    # Filtra por metadado
    filter=lambda record: record["extra"].get("dataset") == "customers",
    format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level}</level> | {message}",
    level="INFO",
    rotation="1 MB",  # Gira o arquivo ao atingir 1MB
    enqueue=True,  # Garante segurança em sistemas com multiprocessamento
)

# Log exclusivo para 'orders'
logger.add(
    "logs/orders.log",
    filter=lambda record: record["extra"].get("dataset") == "orders",
    format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level}</level> | {message}",
    level="INFO",
    rotation="1 MB",
    enqueue=True,
)

# Log exclusivo para 'order_items'
logger.add(
    "logs/order_items.log",
    filter=lambda record: record["extra"].get("dataset") == "order_items",
    format="{time:YYYY-MM-DD HH:mm:ss} | <level>{level}</level> | {message}",
    level="INFO",
    rotation="1 MB",
    enqueue=True,
)


# Decorator que adiciona logging automático a qualquer função
def log_dataset(dataset_name):
    """
    Decorator que registra logs para funções ligadas a um dataset específico.

    Parâmetros:
    ----------
    dataset_name : str
        Nome do dataset associado à função (ex: 'customers', 'orders', etc.)

    Funcionalidade:
    ---------------
    Ao aplicar @log_dataset("customers") em uma função, este decorator:
        - Loga o início da execução com nome da função e argumentos
        - Loga sucesso após a execução
        - Loga erros detalhados se a função falhar
        - Direciona o log para o arquivo correto baseado no dataset

    Uso:
    ----
    @log_dataset("orders")
    def transformar_orders(df):
        ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cria um logger "especializado" com metadado 'dataset'
            bound_logger = logger.bind(dataset=dataset_name)

            # Loga a chamada da função
            bound_logger.info(
                f"Chamando '{func.__name__}' com args={args} kwargs={kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                bound_logger.success(
                    f"'{func.__name__}' executado com sucesso."
                )
                return result
            except Exception as e:
                bound_logger.exception(
                    f"Erro na execução de '{func.__name__}': {e}"
                )
                raise  # Mantém a exceção original

        return wrapper

    return decorator
