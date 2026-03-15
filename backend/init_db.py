"""
数据库初始化脚本
用于创建数据库和表结构
"""
from app.core.database import engine, Base
from app.models import models
from app.core.config import settings

def init_database():
    """初始化数据库，创建所有表"""
    print(f"正在连接到数据库: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print("正在创建数据表...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("数据库初始化完成！")
    print(f"已创建以下表:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        print("\n请检查:")
        print("1. MySQL 服务是否已启动")
        print("2. 数据库是否已创建")
        print("3. .env 文件中的数据库配置是否正确")
