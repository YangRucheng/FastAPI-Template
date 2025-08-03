from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .config import config

DB_USER = config["mysql"]["config"]["user"]
DB_PASSWORD = config["mysql"]["config"]["password"]
DB_HOST = config["mysql"]["config"]["host"]
DB_PORT = config["mysql"]["config"]["port"]
DB_NAME = config["mysql"]["config"]["database"]
DB_CHARSET = config["mysql"]["parameters"]["charset"]
DB_POOL_SIZE = config["mysql"]["parameters"]["pool_size"]

SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=50,
    pool_pre_ping=True,
)


def get_db_engine() -> AsyncEngine:
    """获取数据库引擎实例"""
    return engine


__all__ = ["get_db_engine"]
