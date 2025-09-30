import requests
from functools import lru_cache
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from app.core.config import settings

from app.core.config import settings

@lru_cache(maxsize=1)
def get_keycloak_openid() -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=settings.keycloak_server_url,
        realm_name=settings.keycloak_realm,
        client_id=settings.keycloak_client_id,
        client_secret_key=settings.keycloak_client_secret,
    )

def get_openid_config():
    return get_keycloak_openid().well_known()

@lru_cache(maxsize=1)
def get_jwks():
    jwks_url = (
        f"{settings.keycloak_server_url}"
        f"realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    )
    response = requests.get(jwks_url, timeout=5)
    response.raise_for_status()
    return response.json()

def get_keycloak_admin() -> KeycloakAdmin:
    if settings.keycloak_use_service_account:
        try:
            return KeycloakAdmin(
                server_url=settings.keycloak_server_url,
                realm_name=settings.keycloak_realm,
                client_id=settings.keycloak_client_id,
                client_secret_key=settings.keycloak_client_secret,
                verify=True,
            )
        except KeycloakAuthenticationError:
            pass

    if settings.keycloak_admin_username and settings.keycloak_admin_password:
        return KeycloakAdmin(
            server_url=settings.keycloak_server_url,
            realm_name=settings.keycloak_realm,
            user_realm_name=settings.keycloak_realm,
            username=settings.keycloak_admin_username,
            password=settings.keycloak_admin_password,
            verify=True,
        )

    raise RuntimeError(
        "Keycloak admin not configured: enable service account or set "
        "KEYCLOAK_ADMIN_USERNAME/KEYCLOAK_ADMIN_PASSWORD."
    )
