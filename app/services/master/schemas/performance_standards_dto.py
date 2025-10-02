from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class PerformanceStandardsEvaluationMethod(str, Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"

class PerformanceStandardsBase(BaseModel):
    category_id: str = Field(..., example="uuid-category-id")
    name: str = Field(..., min_length=1, max_length=150, example="Nama Standar")
    description: Optional[str] = Field(None, example="Deskripsi Standar")
    evaluation_method: PerformanceStandardsEvaluationMethod = Field(..., example="MANUAL")
    scoring_rules: Optional[Any] = Field(None, example={"rule": "value"})
    evaluation_guide: Optional[str] = Field(None, example="Panduan Penilaian PM")
    weight_percentage: float = Field(..., example=10.0)

    model_config = {"from_attributes": True}

class PerformanceStandardsAdd(PerformanceStandardsBase):
    created_by: Optional[str] = Field(None, example="user_id")

class PerformanceStandardsUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    evaluation_method: Optional[PerformanceStandardsEvaluationMethod] = None
    scoring_rules: Optional[Any] = None
    evaluation_guide: Optional[str] = None
    weight_percentage: Optional[float] = None

    model_config = {"from_attributes": True}

class PerformanceStandardsResponse(PerformanceStandardsBase):
    id: str
    created_by: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
