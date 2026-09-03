from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "SMARTPRUEBA"
    PROJECT_VERSION: str = "0.0.1"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str

    # Genera uno nuevo con: python -c "import secrets; print(secrets.token_urlsafe(64))"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
