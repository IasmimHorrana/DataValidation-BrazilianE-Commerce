import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega variáveis do arquivo .env
load_dotenv(dotenv_path="../.env")

# Recupera as variáveis de ambiente com dados do banco
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Cria a engine do SQLAlchemy para conexão com o banco PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)
