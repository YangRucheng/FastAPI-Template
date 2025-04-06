from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import datetime
import uvicorn
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, redoc_url=None, docs_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse("https://cdn.micono.eu.org/icon/logo.png", status_code=301)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse("https://www.baidu.com", status_code=302)
    else:
        return JSONResponse(
            {
                "status": -1,
                "msg": exc.detail,
                "data": None,
                "time": int(datetime.datetime.now().timestamp()),
            },
            status_code=exc.status_code,
        )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        {
            "status": -1,
            "msg": "服务器内部错误!",
            "time": int(datetime.datetime.now().timestamp()),
        },
        status_code=500,
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    starttime = datetime.datetime.now()
    response: Response = await call_next(request)
    endtime = datetime.datetime.now()
    response.headers["X-Process-Time"] = (
        f"{(endtime - starttime).total_seconds():.5f} s"
    )
    response.headers["X-Client-Host"] = request.client.host
    return response


if __name__ == "__main__":
    from utils.config import config
    from utils.logger import set_log_formatter

    starttime = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
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
                ("X-Copyright", "© 2024 Misaka Network Studio. All rights reserved."),
                ("X-Server-Start-Time", starttime),
            ],
        )
    except KeyboardInterrupt:
        logging.info("Ctrl+C 终止服务")
