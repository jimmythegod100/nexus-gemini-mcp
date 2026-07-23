import logging
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "nexus-gemini-mcp"
    SERVICE_PORT: int = 8001
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: str = "test-key"
    GEMINI_MODEL: str = "gemini-pro"
    REQUEST_TIMEOUT: int = 300
    MAX_RETRIES: int = 3
    DATABASE_URL: str = "postgresql://nexus_user:nexus_password@localhost:5432/nexus"
    REDIS_URL: str = "redis://localhost:6379/0"
    MCP_PROTOCOL: str = "stdio"
    MCP_VERSION: str = "1.0"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


def setup_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
