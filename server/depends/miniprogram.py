from typing import Literal, Optional
from fastapi import Depends, Request


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


__all__ = [
    "GetAppInfo",
    "AppInfo",
]
