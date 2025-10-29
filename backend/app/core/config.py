from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env files."""

    app_name: str = "LLM + CV Automation Backend"
    environment: str = "development"
    api_prefix: str = "/v1"
    allowed_domains: List[str] = ["https://example.com"]
    vlm_provider: str = "off"
    cost_budget_cents: int = 500
    action_timeout_seconds: int = 60
    run_timeout_seconds: int = 600
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/llm_cv"
    redis_url: str = "redis://localhost:6379/0"
    s3_endpoint: Optional[str] = None
    s3_bucket: str = "llm-cv-artifacts"
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    traces_root: Path = Path("./artifacts")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings."""

    settings = Settings()  # type: ignore[call-arg]
    settings.traces_root.mkdir(parents=True, exist_ok=True)
    return settings

