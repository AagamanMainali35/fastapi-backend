from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    DEBUG: bool = False

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str = "FastAPI App"
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    VERIFICATION_CODE_EXPIRE_MINUTES: int = 10

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


settings = Settings()
