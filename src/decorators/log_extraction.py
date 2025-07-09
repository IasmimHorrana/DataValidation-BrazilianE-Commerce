from functools import wraps

from loguru import logger


def log_csv_extraction(log_file: str):
    def decorator(func):
        logger.add(
            log_file,
            format="{time} | {level} | {message}",
            level="INFO",
            rotation="1 MB",
            enqueue=True,
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Iniciando leitura: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.success(
                    f"Leitura finalizada com sucesso. Linhas: {len(result)}"
                )
                return result
            except Exception as e:
                logger.exception(f"Erro ao executar {func.__name__}: {e}")
                raise

        return wrapper

    return decorator
