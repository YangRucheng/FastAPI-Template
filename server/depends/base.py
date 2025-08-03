from fastapi import Depends
import httpx


from utils import database

from .const import HEADER

client = httpx.AsyncClient(
    headers=HEADER,
    timeout=None,
    verify=False,
    http2=True,
)


def GetDbEngine() -> Depends:
    """获取数据库引擎实例"""
    return Depends(database.get_db_engine)


def GetClient() -> Depends:
    """获取 httpx 客户端实例"""

    def _get_client() -> httpx.AsyncClient:
        return client

    return Depends(_get_client)
