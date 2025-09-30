from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserInfo(BaseModel):
    id: str
    preferred_username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: List[str] = []

class ChangeProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class ChangeProfileResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
