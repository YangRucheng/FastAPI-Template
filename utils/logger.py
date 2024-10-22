from types import FrameType
from loguru import logger
from typing import cast
import logging
import sys


logger.remove(0)

logger.add(
    sys.stdout,
    format="<green>{time:YYYY/MM/DD HH:mm:ss.SSS}</green> | "
           "<level>{level: <7}</level> | "
           "<cyan>{name: <10}</cyan> | "
           "<white>{message}</white>",
    level="INFO",
)

# logger.add(
#     'main.log',
#     level="INFO",
#     serialize=True,
# )


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


for name in ['uvicorn', 'uvicorn.error', 'uvicorn.access', 'uvicorn.server']:
    _logger = logging.getLogger(name)
    _logger.setLevel("INFO")
    _logger.handlers = []
    if "." not in name:
        _logger.addHandler(InterceptHandler())
