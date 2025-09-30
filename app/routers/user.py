from fastapi import APIRouter, status, Depends
from app.services.user.user import UserService
from app.services.user.schemas.change_password import ChangePasswordRequest
from app.services.user.schemas.profile import ChangeProfileRequest, UserInfo
from app.utils.response.response import success_response
from app.middlewares.auth import get_current_user

router = APIRouter(prefix="/user")

@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK
)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: UserInfo = Depends(get_current_user),
):
    result = UserService.change_password(current_user.id, payload)
    return success_response(
        data=result,
        message="Password berhasil diubah",
        status_code=status.HTTP_200_OK
    )

@router.patch(
    "/me/profile",
    status_code=status.HTTP_200_OK
)
async def update_profile(
    payload: ChangeProfileRequest,
    current_user: UserInfo = Depends(get_current_user),
):
    result = UserService.update_profile(current_user.id, payload)
    return success_response(
        data=result,
        message="Profil berhasil diperbarui",
        status_code=status.HTTP_200_OK,
    )

@router.get("/me")
async def get_current_user(current_user: UserInfo = Depends(get_current_user)):
    return success_response(
        message="User info retrieved successfully",
        data=current_user
    )
