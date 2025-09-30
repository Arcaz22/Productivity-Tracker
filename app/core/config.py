from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    keycloak_server_url: str = Field(..., env="KEYCLOAK_SERVER_URL")
    keycloak_realm: str = Field(..., env="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(..., env="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(..., env="KEYCLOAK_CLIENT_SECRET")
    keycloak_admin_username: Optional[str] = Field(None, env="KEYCLOAK_ADMIN_USERNAME")
    keycloak_admin_password: Optional[str] = Field(None, env="KEYCLOAK_ADMIN_PASSWORD")
    keycloak_use_service_account: bool = Field(True, env="KEYCLOAK_USE_SERVICE_ACCOUNT")
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
