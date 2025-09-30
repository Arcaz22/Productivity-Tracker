import traceback
from typing import Any, Dict

from fastapi import status
from keycloak import KeycloakPostError

from app.core.clients import get_keycloak_admin
from app.services.user.schemas.profile import ChangeProfileRequest, ChangeProfileResponse
from app.services.user.schemas.change_password import ChangePasswordRequest

from app.utils.response.exception import APIException

class UserService:
    @staticmethod
    def change_password(user_id: str, payload: ChangePasswordRequest) -> None:
        if payload.new_password != payload.new_password_confirmation:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Konfirmasi password baru tidak sama"
            )

        admin = get_keycloak_admin()
        try:
            admin.set_user_password(
                user_id=user_id,
                password=payload.new_password,
                temporary=False
            )
            try:
                admin.logout(user_id)
            except Exception:
                pass

            return None 
        except KeycloakPostError as e:
            raise APIException(
                status.HTTP_400_BAD_REQUEST,
                message=f"Gagal mengubah password: {e}"
            )
        except Exception as e:
            raise APIException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Kesalahan internal: {e}"
            )

    @staticmethod
    def update_profile(user_id: str, payload: ChangeProfileRequest) -> ChangeProfileResponse:
        if payload.first_name is None and payload.last_name is None and payload.email is None:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Tidak ada field yang diubah")

        admin = get_keycloak_admin()
        body = {}
        if payload.first_name is not None:
            body["firstName"] = payload.first_name
        if payload.last_name is not None:
            body["lastName"] = payload.last_name
        if payload.email is not None:
            body["email"] = payload.email
            body["emailVerified"] = False

        try:
            if body:
                admin.update_user(user_id=user_id, payload=body)

            updated_user = admin.get_user(user_id)
            first_name = updated_user.get("firstName") or updated_user.get("first_name")
            last_name = updated_user.get("lastName") or updated_user.get("last_name")
            email = updated_user.get("email")

            return ChangeProfileResponse(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
        except KeycloakPostError as e:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message=f"Gagal update profil: {e}")
        except Exception as e:
            print(f"ERROR updating profile: {str(e)}")
            print(traceback.format_exc())
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Kesalahan internal: {e}")
