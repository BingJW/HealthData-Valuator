from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_database_url, settings

# 数据库连接配置 (MySQL)
SQLALCHEMY_DATABASE_URL = get_database_url()

# 创建数据库引擎
# MySQL 连接池配置
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # 连接前检查连接是否有效
    echo=False  # 设置为 True 可以看到 SQL 语句
)

# 创建 SessionLocal 类，以后每个请求会有一个独立的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类，后面的模型（User, Evaluation）都会继承它
Base = declarative_base()

# 获取数据库连接的工具函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()