from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth.auth import AuthService
from app.services.user.schemas.profile import UserInfo

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInfo:
    token = credentials.credentials
    return AuthService.verify_token(token)
