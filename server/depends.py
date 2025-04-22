from typing import Literal, Optional
from fastapi import Depends, Request
import httpx

from utils import database


class AppInfo:
    """请求来源小程序"""

    appid: str
    version: Literal["release", "trial", "devtools"]

    def __init__(self, appid: str, version: str):
        self.appid = appid

        if version == "devtools":
            self.version = "devtools"
        elif version == "0":
            self.version = "trial"
        else:
            self.version = "release"


def GetAppInfo() -> Depends:
    """获取请求来源小程序"""

    def _get_appinfo(request: Request) -> Optional[AppInfo]:
        referer = request.headers.get("Referer", "")
        _list = referer.split("/")

        if len(_list) < 5:
            return None

        return AppInfo(
            appid=_list[3],
            version=_list[4],
        )

    return Depends(_get_appinfo)


def GetDbEngine() -> Depends:
    """获取数据库引擎实例"""
    return Depends(database.get_db_engine)


HEADER = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
    "Referer": "https://mobilelearn.chaoxing.com",
}

client = httpx.AsyncClient(
    headers=HEADER,
    timeout=None,
    verify=False,
    http2=True,
)


def GetClient() -> Depends:
    """获取 httpx 客户端实例"""

    def _get_client() -> httpx.AsyncClient:
        return client

    return Depends(_get_client)


__all__ = [
    "GetAppInfo",
    "GetDbEngine",
    "GetClient",
    "AppInfo",
    "client",
]
