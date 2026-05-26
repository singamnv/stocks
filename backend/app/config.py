from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Always read from backend/.env regardless of where the process was started.
BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    FINNHUB_API_KEY: str = ""
    CORS_ORIGIN: str = "http://localhost:5173"
    ANTHROPIC_API_KEY: str = ""
    ADMIN_TOKEN: str = ""


settings = Settings()
