from typing import Optional
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middlewares.rbac import require_roles
from app.services.master.performance_standards_dto import PerformanceStandardService
from app.services.master.schemas.performance_standards_dto import (
    PerformanceStandardsAdd,
    PerformanceStandardsResponse,
    PerformanceStandardsUpdate,
)
from app.services.user.schemas.profile import UserInfo
from app.utils.response.response import paginated_response, success_response

router = APIRouter(prefix="/performance_standards")

@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
)
async def add_performance_standards(
    payload: PerformanceStandardsAdd,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    ps = PerformanceStandardService.add_performance_standards(db, payload, current_user.id)
    return success_response(
        data=PerformanceStandardsResponse.model_validate(ps),
        message="Performance standards created successfully",
        status_code=status.HTTP_201_CREATED,
    )

@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
)
async def list_performance_standards(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    filter: str = Query(None),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    category_id: Optional[str] = Query(None),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    items, total = PerformanceStandardService.list_performance_standards(
        db, page, limit, filter, sort_order, category_id
    )
    return paginated_response(
        items=[
            PerformanceStandardsResponse.model_validate(r)
            for r in items
        ],
        total=total,
        page=page,
        limit=limit,
        filters=(
            {"filter": filter, "sort_order": sort_order, "category_id": category_id}
            if filter or category_id is not None
            else None
        ),
    )

@router.put(
    "/{performance_standards_id}",
    status_code=status.HTTP_200_OK,
)
async def update_performance_standards(
    payload: PerformanceStandardsUpdate,
    performance_standards_id: str = Path(..., description="Performance Standards ID"),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    ps = PerformanceStandardService.update_performance_standards(db, performance_standards_id, payload, current_user.id)
    return success_response(
        data=PerformanceStandardsResponse.model_validate(ps),
        message="Performance standards updated successfully",
        status_code=status.HTTP_200_OK,
    )

@router.delete(
    "/{performance_standards_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_performance_standards(
    performance_standards_id: str = Path(..., description="Performance Standards ID"),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    PerformanceStandardService.delete_performance_standards(db, performance_standards_id, current_user.id)
    return success_response(
        message="Performance standards deleted successfully",
        status_code=status.HTTP_200_OK,
    )
