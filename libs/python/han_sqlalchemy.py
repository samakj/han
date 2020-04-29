from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_database(
    host: str, port: int, user: str, dbname: str, password: str
) -> Engine:
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
