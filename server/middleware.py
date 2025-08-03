from starlette.types import Scope, Receive, Send, ASGIApp
from typing import Dict, List
from fastapi import Request
import threading
import httpx
import time

client = httpx.AsyncClient(http2=True, timeout=5.0)


def RealIPMiddleware(app: ASGIApp) -> ASGIApp:
    """设置真实 IP 中间件"""

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive=receive)
            if x_real_ip := request.headers.get("X-Real-IP"):
                scope["client"] = (x_real_ip, scope["client"][1])
            elif x_forwarded_for := request.headers.get("X-Forwarded-For"):
                scope["client"] = (x_forwarded_for.split(",")[0], scope["client"][1])

        await app(scope, receive, send)

    return middleware


ip_address = {}


def RealIPAddressMiddleware(app: ASGIApp) -> ASGIApp:
    """设置真实 IP 和注入归属地中间件"""

    async def get_address(ip: str) -> str:
        global ip_address
        if ip in ip_address:
            return ip_address[ip]

        resp = await client.get(
            url="https://api.map.baidu.com/location/ip",
            params={
                "ip": ip,
                "coor": "gcj02",
                "ak": "xYjRz7D6pjc3xV516qReaRgcTdoZTyxP",
            },
        )
        res: dict = resp.json()

        ip_address[ip] = res.get("content", {}).get("address", "未知")
        return ip_address[ip]

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive=receive)
            if x_real_ip := request.headers.get("x-real-ip"):
                scope["client"] = (x_real_ip, scope["client"][1])
            elif x_forwarded_for := request.headers.get("x-forwarded-for"):
                scope["client"] = (x_forwarded_for.split(",")[0], scope["client"][1])

            address = await get_address(scope["client"][0])
            request.state["address"] = address

        await app(scope, receive, send)

    return middleware


def ProcessTimeMiddleware(app: ASGIApp) -> ASGIApp:
    """设置接口耗时计算中间件"""

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            start_time = time.time()

            async def send_wrapper(message: dict) -> None:
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    headers: list = message.get("headers", [])
                    headers.append(
                        (b"X-Process-Time", str(process_time).encode("utf-8"))
                    )
                    message["headers"] = headers
                await send(message)

            await app(scope, receive, send_wrapper)
        else:
            await app(scope, receive, send)

    return middleware


request_timestamps: Dict[str, List[float]] = {}
request_timestamps_lock = threading.Lock()


def RateLimitMiddleware(
    app: ASGIApp,
    *,
    rate: int = 30,  # 最多 30 次请求
    window: int = 10,  # 滑动窗口 10 秒
    block: bool = True,
    key_prefix: str = "rate_limit",
):
    """接口限流中间件"""

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            client_ip = scope["client"][0]
            key = f"{key_prefix}:{client_ip}"
            now = time.time()
            with request_timestamps_lock:
                if key in request_timestamps:
                    request_timestamps[key] = [
                        ts for ts in request_timestamps[key] if ts > now - window
                    ]
                else:
                    request_timestamps[key] = []
                if len(request_timestamps[key]) >= rate:
                    if block:
                        await send(
                            {
                                "type": "http.response.start",
                                "status": 429,
                                "headers": [],
                            }
                        )
                        await send({"type": "http.response.body", "body": b""})
                        return
                if key not in request_timestamps:
                    request_timestamps[key] = [now]
                else:
                    request_timestamps[key].append(now)
        await app(scope, receive, send)

    return middleware
