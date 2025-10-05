from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import status

from app.models.activity_cateories import ActivityCategories
from app.models.performance_standards import PerformanceStandards
from app.services.master.schemas.performance_standards_dto import PerformanceStandardsAdd, PerformanceStandardsUpdate
from app.utils.response.exception import APIException


class PerformanceStandardService:
    @staticmethod
    def add_performance_standards(db: Session, data: PerformanceStandardsAdd, user_id: str) -> PerformanceStandards:
        # Pastikan kategori aktivitas ada
        category = db.query(ActivityCategories).filter(
            ActivityCategories.id == data.category_id,
            ActivityCategories.deleted_at.is_(None)
        ).first()
        if not category:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Activity category not found",
            )
        existing = db.query(PerformanceStandards).filter(
            PerformanceStandards.name.ilike(data.name),
            PerformanceStandards.category_id == data.category_id,
            PerformanceStandards.deleted_at.is_(None),
        ).first()
        if existing:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Performance standards name already exists in this category",
            )
        ps = PerformanceStandards(
            name=data.name,
            category_id=data.category_id,
            description=data.description,
            evaluation_method=data.evaluation_method,
            scoring_rules=data.scoring_rules,
            evaluation_guide=data.evaluation_guide,
            weight_percentage=data.weight_percentage,
            created_by=user_id,
            updated_by=user_id,
        )
        db.add(ps)
        db.commit()
        db.refresh(ps)
        return ps

    @staticmethod
    def list_performance_standards(
        db: Session,
        page: int = 1,
        limit: int = 10,
        filter: Optional[str] = None,
        sort_order: str = "asc",
        category_id: Optional[str] = None,
    ) -> Tuple[List[PerformanceStandards], int]:
        query = db.query(PerformanceStandards).filter(PerformanceStandards.deleted_at.is_(None))
        if category_id:
            query = query.filter(PerformanceStandards.category_id == category_id)
        if filter:
            query = query.filter(
                or_(
                    PerformanceStandards.name.ilike(f"%{filter}%"),
                    PerformanceStandards.description.ilike(f"%{filter}%"),
                )
            )
        if sort_order == "desc":
            query = query.order_by(PerformanceStandards.name.desc())
        else:
            query = query.order_by(PerformanceStandards.name.asc())
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    @staticmethod
    def update_performance_standards(db: Session, performance_standards_id: str, data: PerformanceStandardsUpdate, user_id: str) -> PerformanceStandards:
        ps = db.query(PerformanceStandards).filter(
            PerformanceStandards.id == performance_standards_id,
            PerformanceStandards.deleted_at.is_(None)
        ).first()
        if not ps:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Performance standards not found",
            )
        if data.name and data.name != ps.name:
            existing = db.query(PerformanceStandards).filter(
                PerformanceStandards.name.ilike(data.name),
                PerformanceStandards.category_id == ps.category_id,
                PerformanceStandards.id != ps.id,
                PerformanceStandards.deleted_at.is_(None),
            ).first()
            if existing:
                raise APIException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Performance standards name already exists in this category",
                )
            ps.name = data.name
        if data.description is not None:
            ps.description = data.description
        if data.evaluation_method is not None:
            ps.evaluation_method = data.evaluation_method
        if data.scoring_rules is not None:
            ps.scoring_rules = data.scoring_rules
        if data.evaluation_guide is not None:
            ps.evaluation_guide = data.evaluation_guide
        if data.weight_percentage is not None:
            ps.weight_percentage = data.weight_percentage
        ps.updated_by = user_id
        db.commit()
        db.refresh(ps)
        return ps

    @staticmethod
    def delete_performance_standards(db: Session, performance_standards_id: str, user_id: str) -> None:
        ps = db.query(PerformanceStandards).filter(
            PerformanceStandards.id == performance_standards_id,
            PerformanceStandards.deleted_at.is_(None)
        ).first()
        if not ps:
            raise APIException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Performance standards not found",
            )
        ps.deleted_at = datetime.now()
        ps.updated_by = user_id
        db.commit()
