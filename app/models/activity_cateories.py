from sqlalchemy import Column, String, Boolean
from app.utils.base_model import BaseModel

class ActivityCategories(BaseModel):
    __tablename__ = "ref_activity_categories"

    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
