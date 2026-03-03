from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base 

# 1. 用户表：存储基本账号信息
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255)) 
    hospital = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    evaluations = relationship("Evaluation", back_populates="owner")

# 2. 评估任务表：记录测算的总价值
class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_value = Column(Numeric(15, 2))
    status = Column(String(20), default='draft')
    owner = relationship("User", back_populates="evaluations")
    indicators = relationship("IndicatorData", back_populates="evaluation")

# 3. 指标明细表：存储系统设计中的 9 类核心指标金额
class IndicatorData(Base):
    __tablename__ = "indicator_data"
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey('evaluations.id'))
    category = Column(Integer) # 1-9 代表不同类别
    item_name = Column(String(100))
    amount = Column(Numeric(12, 2))
    evaluation = relationship("Evaluation", back_populates="indicators")