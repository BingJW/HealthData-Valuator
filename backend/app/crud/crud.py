from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas

def create_evaluation(db: Session, evaluation: schemas.EvaluationCreate, user_id: int):
    """
    创建测算记录逻辑：
    1. 计算所有子项指标金额的总和
    2. 持久化评估主任务
    3. 批量记录各项指标明细数据
    """
    # 遍历指标列表并累加金额
    total = sum(item.amount for item in evaluation.indicators)
    
    # 创建并保存评估主记录
    db_eval = models.Evaluation(
        user_id=user_id,
        evaluation_name=evaluation.evaluation_name, 
        total_value=total,
        status="completed"
    )
    db.add(db_eval)
    db.commit()      # 提交以生成主表自增ID
    db.refresh(db_eval)
    
    # 循环写入指标明细，建立与主记录的关联
    for item in evaluation.indicators:
        db_indicator = models.IndicatorData(
            evaluation_id=db_eval.id,
            category=item.category,
            item_name=item.item_name,
            amount=item.amount
        )
        db.add(db_indicator)
    
    db.commit() # 提交所有指标明细数据
    return db_eval

def get_user_by_username(db: Session, username: str):
    """根据用户名检索用户对象"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """执行新用户注册逻辑"""
    db_user = models.User(
        username=user.username,
        password=user.password,
        hospital=user.hospital
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user