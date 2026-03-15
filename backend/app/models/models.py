from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    """用户信息表，存储系统基本账户信息"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    hospital = Column(String(200), nullable=True)

    # 关联用户的评估测算记录
    evaluations = relationship("Evaluation", back_populates="owner")

class Evaluation(Base):
    """评估任务主表，记录单次测算的总值与状态"""
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    evaluation_name = Column(String(200), index=True) 
    total_value = Column(Float)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User", back_populates="evaluations")
    # 关联该评估任务下的所有具体指标明细
    indicators = relationship("IndicatorData", back_populates="evaluation")

class IndicatorData(Base):
    """指标明细表，存储 9 大类清单中的具体子项数据"""
    __tablename__ = "indicator_data"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    category = Column(Integer)  # 指标分类代号 (1-9)
    item_name = Column(String(200))   # 指标具体子项名称
    amount = Column(Float)       # 评估金额

    evaluation = relationship("Evaluation", back_populates="indicators")