from fastapi.responses import JSONResponse, RedirectResponse
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import datetime
import uvicorn
import logging
import time

from middleware import RealIPMiddleware, ProcessTimeMiddleware
from depends import client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await client.aclose()


app = FastAPI(lifespan=lifespan, redoc_url=None, docs_url=None)

app.add_middleware(RealIPMiddleware)
app.add_middleware(ProcessTimeMiddleware)


@app.get("/")
@app.get("/favicon.ico")
async def favicon() -> RedirectResponse:
    return RedirectResponse("https://cdn.micono.eu.org/icon/logo.png", status_code=301)


@app.exception_handler(HTTPException)
async def _(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse("https://www.baidu.com", status_code=302)
    else:
        return JSONResponse(
            {
                "status": -1,
                "msg": exc.detail,
                "data": None,
                "time": int(time.time()),
            },
            status_code=exc.status_code,
        )


@app.exception_handler(Exception)
async def _(request: Request, exc: Exception):
    return JSONResponse(
        {
            "status": -1,
            "msg": "网络拥挤, 请稍后再试!",
            "time": int(time.time()),
        },
        status_code=500,
    )


if __name__ == "__main__":
    from utils.config import config
    from utils.logger import set_log_formatter

    now = datetime.datetime.now()
    set_log_formatter()

    try:
        uvicorn.run(
            app="app:app",
            host=config["scheme"]["address"],
            port=config["scheme"]["port"],
            reload=False,
            forwarded_allow_ips="172.16.0.0/12",
            log_config=None,
            workers=1,
            headers=[
                ("X-Server-Start-Time", now.strftime(r"%Y-%m-%d %H:%M:%S")),
            ],
        )
    except KeyboardInterrupt:
        logging.info("Ctrl+C 终止服务")
