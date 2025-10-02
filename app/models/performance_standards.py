from sqlalchemy import Column, String, Text, Enum, JSON, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.utils.base_model import BaseModel

class PerformanceStandardsEvaluationMethod(enum.Enum):
    MANUAL = "MANUAL"
    SYSTEM = "SYSTEM"

class PerformanceStandards(BaseModel):
    __tablename__ = "ref_performance_standards"

    category_id = Column(UUID(as_uuid=True), ForeignKey("ref_activity_categories.id"), nullable=False, comment="ID Kategori Aktivitas")
    name = Column(String, nullable=False, comment="Nama Standar")
    description = Column(Text, nullable=True, comment="Deskripsi Standar")
    evaluation_method = Column(
        Enum(
            PerformanceStandardsEvaluationMethod,
            name="performancestandardsevaluationmethod"
        ),
        nullable=False,
        comment="Metode Penilaian"
    )
    scoring_rules = Column(JSON, nullable=True, comment="Aturan Penilaian Sistem (JSON)")
    evaluation_guide = Column(Text, nullable=True, comment="Panduan Penilaian PM")
    weight_percentage = Column(DECIMAL(5, 2), nullable=False, comment="Bobot Persentase")

    activity_category = relationship("ActivityCategories", backref="performance_standards")
