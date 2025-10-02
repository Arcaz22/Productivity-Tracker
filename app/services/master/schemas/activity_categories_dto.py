from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ActivityCategoriesBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, example="test")

    model_config = {"from_attributes": True}


class ActivityCategoriesAdd(ActivityCategoriesBase):
    pass


class ActivityCategoriesUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150, example="test")
    is_active: Optional[bool] = None

    model_config = {"from_attributes": True}


class ActivityCategoriesResponse(ActivityCategoriesBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
