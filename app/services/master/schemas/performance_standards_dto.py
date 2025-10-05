from datetime import datetime
from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

class PerformanceStandardsEvaluationMethod(str, Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"

class PerformanceStandardsBase(BaseModel):
    category_id: UUID = Field(..., example="59e89eac-b42e-4a19-b220-a7dad5fc3dc9")
    name: str = Field(..., min_length=1, max_length=150, example="Nama Standar")
    description: Optional[str] = Field(None, example="Deskripsi Standar")
    evaluation_method: PerformanceStandardsEvaluationMethod = Field(..., example="MANUAL")
    scoring_rules: Optional[Any] = Field(None, example={"rule": "value"})
    evaluation_guide: Optional[str] = Field(None, example="Panduan Penilaian PM")
    weight_percentage: float = Field(..., example=10.0)

    model_config = {"from_attributes": True}

class PerformanceStandardsAdd(PerformanceStandardsBase):
    pass

class PerformanceStandardsUpdate(BaseModel):
    category_id: Optional[UUID] = Field(None, example="59e89eac-b42e-4a19-b220-a7dad5fc3dc9")
    name: Optional[str] = Field(None, min_length=1, max_length=150, example="Nama Standar")
    description: Optional[str] = Field(None, example="Deskripsi Standar")
    evaluation_method: Optional[PerformanceStandardsEvaluationMethod] = Field(None, example="MANUAL")
    scoring_rules: Optional[Any] = Field(None, example={"rule": "value"})
    evaluation_guide: Optional[str] = Field(None, example="Panduan Penilaian PM")
    weight_percentage: Optional[float] = Field(None, example=10.0)

    model_config = {"from_attributes": True}

class PerformanceStandardsResponse(PerformanceStandardsBase):
    id: UUID
    created_by: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
