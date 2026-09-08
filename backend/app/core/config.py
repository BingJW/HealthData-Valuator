from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from sqlalchemy.engine import URL
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SESSION_HOURS: int = Field(default=12, ge=1, le=720)
    ENABLE_DEMO: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "healthdata_valuator"
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    model_config = SettingsConfigDict(
        # 固定从 backend/.env 读取，避免部署时工作目录不同导致读不到 .env
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8-sig",  # 支持 UTF-8 with BOM
        case_sensitive=True,
        extra="ignore"  # 忽略额外的字段（如 BOM 字符）
    )


settings = Settings()


def get_database_url():
    """URL.create safely handles @, :, / and other characters in passwords."""
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    return URL.create('mysql+pymysql', username=settings.DB_USER,
                      password=settings.DB_PASSWORD, host=settings.DB_HOST,
                      port=settings.DB_PORT, database=settings.DB_NAME,
                      query={'charset': 'utf8mb4'})
