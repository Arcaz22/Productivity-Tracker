from datetime import datetime
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import status
from app.models.activity_cateories import ActivityCategories
from app.services.master.schemas.activity_categories_dto import ActivityCategoriesAdd, ActivityCategoriesUpdate

from app.utils.response.exception import APIException


class ActivityCategoriesService:
    @staticmethod
    def add_activity_categories(db: Session, data: ActivityCategoriesAdd, user_id: str) -> ActivityCategories:
        existing = (
            db.query(ActivityCategories)
            .filter(
                ActivityCategories.name.ilike(data.name),
                ActivityCategories.deleted_at.is_(None),
            )
            .first()
        )
        if existing:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Activity categories name already exists",
            )
        ac = ActivityCategories(
            name=data.name,
            is_active=True,
            created_by=user_id,
            updated_by=user_id,
        )
        db.add(ac)
        db.commit()
        db.refresh(ac)
        return ac

    @staticmethod
    def list_activity_categories(
        db: Session,
        page: int = 1,
        limit: int = 10,
        filter: Optional[str] = None,
        sort_order: str = "asc",
        is_active: Optional[bool] = None,
    ) -> List[ActivityCategories]:
        query = db.query(ActivityCategories).filter(ActivityCategories.deleted_at.is_(None))
        if is_active is not None:
            query = query.filter(ActivityCategories.is_active.is_(is_active))
        if filter:
            query = query.filter(
                or_(
                    ActivityCategories.name.ilike(f"%{filter}%"),
                )
            )
        if sort_order == "desc":
            query = query.order_by(ActivityCategories.name.desc())
        else:
            query = query.order_by(ActivityCategories.name.asc())
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    @staticmethod
    def update_activity_categories(db: Session, activity_categories_id: str, data: ActivityCategoriesUpdate, user_id: str) -> ActivityCategories:
        ac = db.query(ActivityCategories).filter(ActivityCategories.id == activity_categories_id).first()
        if not ac:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Activity categories not found",
            )
        existing = (
            db.query(ActivityCategories)
            .filter(
                ActivityCategories.name.ilike(data.name),
                ActivityCategories.id != ac.id,
            )
            .first()
        )
        if existing:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Activity_Categories name already exists",
            )
        ac.name = data.name
        ac.is_active = data.is_active
        ac.updated_by = user_id
        db.commit()
        db.refresh(ac)
        return ac

    @staticmethod
    def delete_activity_categories(db: Session, activity_categories_id: str, user_id: str) -> None:
        ac = db.query(ActivityCategories).filter(ActivityCategories.id == activity_categories_id).first()
        if not ac:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Activity categories not found",
            )
        ac.deleted_at = datetime.now()
        ac.updated_by = user_id
        db.commit()
