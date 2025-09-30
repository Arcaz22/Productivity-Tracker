from typing import Any, Dict, Optional
import uuid
import time
import os

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

IS_DEBUG = os.getenv("DEBUG", "false").lower() == "true"


class APIException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        error_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.error_id = error_id or str(uuid.uuid4())
        self.details = details
        self.timestamp = int(time.time())


async def api_exception_handler(request: Request, exc: APIException):
    response_content = {
        "error_id": exc.error_id,
        "timestamp": exc.timestamp,
        "status_code": exc.status_code,
    }

    if IS_DEBUG or exc.status_code < 500:
        response_content["message"] = exc.message
        if exc.details:
            response_content["details"] = exc.details
    else:
        response_content["message"] = "Internal server error"

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_id = str(uuid.uuid4())
    timestamp = int(time.time())

    response_content = {
        "error_id": error_id,
        "timestamp": timestamp,
        "status_code": exc.status_code,
    }

    if IS_DEBUG or exc.status_code < 500:
        response_content["message"] = exc.detail
    else:
        response_content["message"] = "Internal server error"

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_id = str(uuid.uuid4())
    timestamp = int(time.time())

    response_content = {
        "error_id": error_id,
        "timestamp": timestamp,
        "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": "Validation error on request data",
    }

    if IS_DEBUG:
        response_content["details"] = {"errors": exc.errors()}

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_content,
    )
