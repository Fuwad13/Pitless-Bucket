from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    WEB_CLIENT_ID: str
    WEB_CLIENT_SECRET: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
