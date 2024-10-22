from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql import text

from config import config

DB_USER = config["mysql"]["user"]
DB_PASSWORD = config["mysql"]["password"]
DB_HOST = config["mysql"]["host"]
DB_PORT = config["mysql"]["port"]
DB_NAME = config["mysql"]["database"]
DB_CHARSET = config["mysql"]["parameters"]["charset"]
DB_POOL_SIZE = config["mysql"]["parameters"]["pool_size"]

SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=DB_POOL_SIZE, max_overflow=50)
