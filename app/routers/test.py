from fastapi import APIRouter, Depends
from app.middlewares.rbac import require_roles
from app.services.user.schemas.profile import UserInfo

router = APIRouter(prefix="/test")

@router.get("/admin")
async def admin(current_user: UserInfo = Depends(require_roles(["admin"]))):
    return {"message": "Hello Admin!"}

@router.get("/pm")
async def pm(current_user: UserInfo = Depends(require_roles(["pm"]))):
    return {"message": "Hello Project Manager or Developer!"}

@router.get("/dev")
async def dev(current_user: UserInfo = Depends(require_roles(["dev"]))):
    return {"message": "Hello Developer!"}
