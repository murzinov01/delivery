"""Custom error handlers."""

import json
import traceback
import typing

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError


async def catch_exceptions_middleware(request: Request, call_next: typing.Callable) -> typing.Any:  # noqa: ANN401
    try:
        return await call_next(request)
    except Exception as exc:  # noqa: BLE001
        if isinstance(exc, ValidationError):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_msg: str = str(exc)
        error_message: dict[str, str] = {
            "error_type": str(type(exc).__name__),
            "error": error_msg if error_msg else traceback.format_exc(limit=1),
            "traceback": traceback.format_exc(),
        }
        logger.error(json.dumps(error_message, indent=2))
        error_message.pop("traceback")

        return JSONResponse(error_message, status_code=status_code)
