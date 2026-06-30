from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ledger.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_EXPIRY_DAYS: int = 7
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings():
    return Settings()
