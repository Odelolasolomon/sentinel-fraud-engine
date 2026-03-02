from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection Engine"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # In a real production app, these would come from environment variables
    SECRET_KEY: str = "A_VERY_SECRET_KEY_FOR_JWT_OR_CHALLENGES"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"
    
    # Backend URL for CORS and other links
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
