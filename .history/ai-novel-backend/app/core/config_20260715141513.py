"""
应用配置管理
使用 pydantic-settings 从 .env 文件加载配置
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """应用配置类"""

    # ---- 应用基础 ----
    APP_NAME: str = "AI Novel Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ---- 服务器 ----
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # ---- 数据库 ----
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/ai_novel"

    # ---- Redis ----
    REDIS_URL: str = "redis://localhost:6379/0"

    # ---- 认证 ----
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # ---- AI / LLM ----
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    DEFAULT_MODEL: str = "gpt-4"

    # ---- CORS ----
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ---- 日志 ----
    LOG_LEVEL: str = "INFO"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = Settings()
