from typing import Optional
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middlewares.rbac import require_roles
from app.services.master.activity_categories_svc import ActivityCategoriesService
from app.services.master.schemas.activity_categories_dto import ActivityCategoriesAdd, ActivityCategoriesResponse, ActivityCategoriesUpdate
from app.services.user.schemas.profile import UserInfo
from app.utils.response.response import paginated_response, success_response

router = APIRouter(prefix="/activity_categories")


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
)
async def add_activity_categories(
    payload: ActivityCategoriesAdd,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    ac = ActivityCategoriesService.add_activity_categories(db, payload, current_user.id)
    return success_response(
        data=ActivityCategoriesResponse.model_validate(ac),
        message="Activity categoreis created successfully",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/list",
    status_code=status.HTTP_200_OK,
)
async def list_activity_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    filter: str = Query(None),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    is_active: Optional[bool] = Query(None),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    items, total = ActivityCategoriesService.list_activity_categories(
        db, page, limit, filter, sort_order, is_active
    )
    return paginated_response(
        items=[
            {"id": r.id, "name": r.name, "is_active": r.is_active}
            for r in items
        ],
        total=total,
        page=page,
        limit=limit,
        filters=(
            {"filter": filter, "sort_order": sort_order, "is_active": is_active}
            if filter or is_active is not None
            else None
        ),
    )


@router.put(
    "/{activity_categories_id}",
    status_code=status.HTTP_200_OK,
)
async def update_activity_categories(
    payload: ActivityCategoriesUpdate,
    activity_categories_id: str = Path(..., description="Activity Categories ID"),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    ac = ActivityCategoriesService.update_activity_categories(db, activity_categories_id, payload, current_user.id)
    return success_response(
        data=ActivityCategoriesResponse.model_validate(ac),
        message="Activity categories updated successfully",
        status_code=status.HTTP_200_OK,
    )


@router.delete(
    "/{activity_categories_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_activity_categories(
    activity_categories_id: str = Path(..., description="Activity Categories ID"),
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(require_roles(["pm"]))
):
    ActivityCategoriesService.delete_activity_categories(db, activity_categories_id, current_user.id)
    return success_response(
        message="Activity Categories deleted successfully",
        status_code=status.HTTP_200_OK,
    )
