from fastapi import APIRouter, status, Depends
from app.middlewares.rbac import require_roles
from app.services.auth.auth import AuthService
from app.services.auth.schemas.login import TokenRequest
from app.services.auth.schemas.register import RegisterRequest
from app.services.user.schemas.profile import UserInfo
from app.utils.response.response import success_response

router = APIRouter(prefix="/auth")

@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login(payload: TokenRequest):
    token = AuthService.authenticate_user(payload)
    return success_response(
        data=token,
        message="login berhasil",
        status_code=status.HTTP_200_OK,
    )

@router.post(
    "/add-user",
    status_code=status.HTTP_201_CREATED
)
async def register(
    payload: RegisterRequest,
    current_user: UserInfo = Depends(require_roles(["admin"]))
):
    result = AuthService.register_user(payload)
    return success_response(
        data=result,
        message="berhasil menambahkan akun",
        status_code=status.HTTP_201_CREATED,
    )
