import base64

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str

    FIREBASE_API_KEY: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_PRIVATE_KEY_B64: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str
    FIREBASE_CLIENT_X509_CERT_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("FIREBASE_PRIVATE_KEY_B64", mode="before")
    def decode_private_key(cls, v: str) -> str:
        return base64.b64decode(v).decode("utf-8")


Config = Settings()
