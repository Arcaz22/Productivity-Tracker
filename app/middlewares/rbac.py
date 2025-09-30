from fastapi import Depends, HTTPException, status
from app.middlewares.auth import get_current_user
from app.services.user.schemas.profile import UserInfo

def require_roles(roles: list[str]):
    def role_checker(current_user: UserInfo = Depends(get_current_user)):
        print(f"[RBAC] current_user: {current_user}")  # LOG
        user_roles = getattr(current_user, "roles", [])
        print(f"[RBAC] user_roles: {user_roles}, required: {roles}")  # LOG
        if not any(role in user_roles for role in roles):
            print("[RBAC] Forbidden: user does not have required role")  # LOG
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the required role(s)"
            )
        return current_user
    return role_checker
