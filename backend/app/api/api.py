from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..schemas import schemas
from ..models import models
from ..crud import crud

router = APIRouter()

# 数据库会话依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 模块一：认证模块 (Auth) ---

@router.post("/auth/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    用户注册：创建医院账号
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

# --- 模块二：评估模块 (Evaluation) ---

@router.post("/evaluations")
def calculate_value(
    evaluation: schemas.EvaluationCreate, 
    db: Session = Depends(get_db)
):
    """
    提交测算：接收指标数据并自动入库
    """
    test_user_id = 1 
    result = crud.create_evaluation(db=db, evaluation=evaluation, user_id=test_user_id)
    
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

@router.get("/evaluations")
def get_evaluation_list(db: Session = Depends(get_db)):
    """
    获取列表：返回所有历史记录清单
    """
    evaluations = db.query(models.Evaluation).all()
    return {
        "code": 200,
        "message": "success",
        "data": [
            {
                "id": e.id,
                "evaluation_name": e.evaluation_name,
                "total_value": e.total_value,
                "status": e.status,
                "created_at": e.created_at
            } for e in evaluations
        ]
    }

@router.get("/evaluations/{id}")
def get_evaluation_detail(id: int, db: Session = Depends(get_db)):
    """
    详情报告：返回单次测算的完整明细
    """
    evaluation = db.query(models.Evaluation).filter(models.Evaluation.id == id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="评估记录不存在")
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": evaluation.id,
            "evaluation_name": evaluation.evaluation_name,
            "total_value": evaluation.total_value,
            "created_at": evaluation.created_at,
            "indicators": [
                {
                    "category": i.category,
                    "item_name": i.item_name,
                    "amount": i.amount
                } for i in evaluation.indicators
            ]
        }
    }

@router.delete("/evaluations/{id}")
def delete_evaluation(id: int, db: Session = Depends(get_db)):
    """
    删除记录：从数据库抹掉该次评估
    """
    db_eval = db.query(models.Evaluation).filter(models.Evaluation.id == id).first()
    if not db_eval:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(db_eval)
    db.commit()
    
    return {
        "code": 200,
        "message": "delete success",
        "data": {"id": id}
    }