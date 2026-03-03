from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..schemas import schemas
from ..crud import crud

router = APIRouter()

# 数据库会话依赖项：管理每个请求的数据库连接生命周期
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 核心测算接口：处理医疗数据价值评估
@router.post("/evaluate/")
def calculate_value(
    evaluation: schemas.EvaluationCreate, 
    db: Session = Depends(get_db)
):
    """
    接收评估指标，计算总值，并按照标准的 {code, message, data} 格式返回。
    """
    # 模拟系统当前操作用户
    test_user_id = 1 
    
    # 调用逻辑层进行计算与存储
    result = crud.create_evaluation(
        db=db, 
        evaluation=evaluation, 
        user_id=test_user_id
    )
    
    # 构造统一响应结构，显式映射模型字段以确保 JSON 正确渲染
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": result.id,
            "evaluation_name": result.evaluation_name,
            "total_value": result.total_value,
            "status": result.status,
            "created_at": result.created_at
        }
    }

# 用户管理接口：处理新用户注册
@router.post("/users/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    注册系统用户，并按统一响应格式返回。
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    new_user = crud.create_user(db=db, user=user)
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "hospital": new_user.hospital
        }
    }