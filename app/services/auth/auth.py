import traceback

from typing import Any, Dict

from fastapi import status
from jose import jwt
from keycloak import KeycloakAdmin, KeycloakPostError
from keycloak.exceptions import KeycloakAuthenticationError

from app.core.clients import get_keycloak_openid
from app.core.config import settings
from app.core.clients import get_keycloak_openid, get_keycloak_admin
from app.services.auth.schemas.login import TokenRequest, TokenResponse
from app.services.user.schemas.profile import UserInfo
from app.services.auth.schemas.register import RegisterRequest
from app.utils.response.exception import APIException

# ISSUER = f"{settings.keycloak_server_url}realms/{settings.keycloak_realm}"
# AUDIENCE = settings.keycloak_client_id

class AuthService:
    @staticmethod
    def authenticate_user(payload: TokenRequest) -> TokenResponse:
        try:
            keycloak_openid = get_keycloak_openid()
            token = keycloak_openid.token(payload.username, payload.password)
            return TokenResponse(
                access_token=token["access_token"],
                token_type="bearer",
            )
        except KeycloakAuthenticationError:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid username or password",
            )

    @staticmethod
    def verify_token(token: str) -> UserInfo:
        if not token:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Token tidak diberikan"
            )

        try:
            keycloak_openid = get_keycloak_openid()

            try:
                token_info = keycloak_openid.introspect(token)

                if not token_info.get('active', False):
                    raise APIException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        message="Token tidak aktif"
                    )
            except Exception as introspect_error:
                print(f"Error pada introspect token: {introspect_error}")
                pass

            try:
                claims = jwt.decode(
                    token,
                    key=None,
                    options={
                        "verify_signature": False,
                        "verify_aud": False,
                        "verify_exp": False,
                        "verify_nbf": False,
                        "verify_iat": False,
                        "verify_iss": False
                    }
                )

                print(f"Token claims: {claims.keys()}")

                realm_access = claims.get("realm_access") or {}
                realm_roles = realm_access.get("roles") or []

                resource_access = claims.get("resource_access") or {}
                client_resource = resource_access.get(settings.keycloak_client_id) or {}
                client_roles = client_resource.get("roles") or []

                roles = list(set(realm_roles) | set(client_roles))

                return UserInfo(
                    id=claims.get("sub"),
                    preferred_username=claims.get("preferred_username"),
                    email=claims.get("email"),
                    full_name=claims.get("name") or claims.get("given_name"),
                    roles=roles,
                )
            except jwt.JWTError as jwt_error:
                print(f"JWT decode error: {jwt_error}")
                raise APIException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message=f"Format token tidak valid: {str(jwt_error)}"
                )

        except APIException:
            raise

        except Exception as e:
            print(f"Unexpected error in verify_token: {e}")
            print(traceback.format_exc())
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message=f"Token tidak valid: {str(e)}"
            )

    @staticmethod
    def register_user(payload: RegisterRequest) -> Dict[str, Any]:
        keycloak_admin = get_keycloak_admin()
        try:
            user_id = keycloak_admin.create_user({
                "username": payload.username,
                "email": payload.email,
                "firstName": payload.first_name,
                "lastName": payload.last_name,
                "enabled": True,
                "emailVerified": False,
                "credentials": [{
                    "type": "password",
                    "value": payload.password,
                    "temporary": False,
                }],
            })

            return {
                "message": "User registered successfully",
                "username": payload.username,
                "user_id": user_id,
            }

        except KeycloakPostError as e:
            print("🔑 Keycloak Error:", e)
            error_msg = str(e)
            if "User exists" in error_msg:
                raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Username or email already exists")
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message=f"Registration failed: {error_msg}")

        except Exception as e:
            print("💥 Unexpected Error:", e)
            raise APIException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f"Internal error: {str(e)}")
