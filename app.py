
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import datetime
import uvicorn

from utils.config import config
from utils.logger import logger
from utils import database

ADDRESS = config["scheme"]["address"]
PORT = config["scheme"]["port"]


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
    return RedirectResponse("https://misaka-network.top/favicon.ico", status_code=301)


@app.get("/")
async def index():
    return {
        "status": 0,
        "msg": "Welcome to Misaka Network Studio",
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse("https://misaka-network.top", status_code=302)
    else:
        return JSONResponse({
            "status": -1,
            "msg": exc.detail,
            "data": None,
            "time": int(datetime.datetime.now().timestamp()),
        }, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({
        "status": -1,
        "msg": "参数错误, 请检查参数",
        "data": {
            "body": exc.body,
            "query": {
                "raw": str(request.query_params),
                "parsed": dict(request.query_params),
            },
            "error": exc.errors(),
        },
        "time": int(datetime.datetime.now().timestamp()),
    }, status_code=422)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse({
        "status": -1,
        "msg": "服务器内部错误, 请联系管理员! 邮箱: admin@misaka-network.top",
        "time": int(datetime.datetime.now().timestamp()),
    }, status_code=500)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    starttime = datetime.datetime.now()
    response: Response = await call_next(request)
    endtime = datetime.datetime.now()
    response.headers["X-Process-Time"] = f"{(endtime - starttime).total_seconds():.5f} s"
    response.headers["X-Client-Host"] = request.client.host
    return response

if __name__ == "__main__":
    starttime = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    try:
        uvicorn.run(
            app="app:app",
            host=ADDRESS,
            port=PORT,
            reload=False,
            forwarded_allow_ips="*",
            log_config=None,
            workers=1,
            headers=[
                ("X-Powered-By", "Misaka Network Studio"),
                ("X-Statement", "This service is provided by Misaka Network Studio. For complaints/cooperation, please email admin@misaka-network.top"),
                ("X-Copyright", "© 2024 Misaka Network Studio. All rights reserved."),
                ("X-Server-Start-Time", starttime),
            ],
        )
    except KeyboardInterrupt:
        logger.info("Ctrl+C 终止服务")
