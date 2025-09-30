from typing import Any, Dict, Optional, TypeVar, Generic, List
import time
from fastapi import status
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMeta(BaseModel):
    page: int = Field(1, description="Current page number")
    limit: int = Field(10, description="Number of items per page")
    total: int = Field(0, description="Total number of items")
    filter_applied: Optional[Dict[str, Any]] = Field(
        None, description="Applied filters"
    )


class BaseResponse(BaseModel, Generic[T]):
    model_config = {"ser_json_exclude_none": True}

    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    timestamp: int = Field(
        default_factory=lambda: int(time.time()),
        description="Unix timestamp in seconds",
    )
    data: Optional[T] = Field(None, description="Response data")
    meta: Optional[ResponseMeta] = Field(None, description="Response metadata")


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
) -> Dict[str, Any]:
    resp: Dict[str, Any] = {
        "status_code": status_code,
        "message": message,
        "timestamp": int(time.time()),
    }
    if data is not None:
        resp["data"] = data
    return resp


def paginated_response(
    items: List[Any],
    total: int,
    page: int = 1,
    limit: int = 10,
    message: str = "Data retrieved successfully",
    filters: Optional[Dict[str, Any]] = None,
    status_code: int = status.HTTP_200_OK,
) -> Dict[str, Any]:
    """Dipakai untuk list/search: menyertakan meta."""
    meta: Dict[str, Any] = {"page": page, "limit": limit, "total": total}
    if filters:
        meta["filter_applied"] = filters

    return {
        "status_code": status_code,
        "message": message,
        "timestamp": int(time.time()),
        "data": items,
        "meta": meta,
    }
