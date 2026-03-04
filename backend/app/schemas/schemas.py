from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- 1. 指标明细：对应清单子项 ---
class IndicatorBase(BaseModel):
    category: int = Field(
        ..., 
        ge=1, 
        le=9, 
        description="1:数据战略与治理成本, 2:数据获取与采集成本, 3:数据存储与备份成本, 4:数据处理与加工成本, 5:数据应用与分析成本, 6:数据流通与共享成本, 7:数据安全隐私与合规成本, 8:数据归档与销毁成本, 9:数据全流程人力成本"
    )
    item_name: str = Field(..., description="指标子项的具体名称（如：服务器采购、咨询费等）")
    amount: float = Field(..., ge=0, description="该项评估的具体金额")

# --- 2. 创建评估任务：前端向后端提交数据的格式 ---
class EvaluationCreate(BaseModel):
    evaluation_name: str = Field(..., description="评估任务名称（如：XX医院2026年度测算）")
    indicators: List[IndicatorBase]

# --- 3. 返回评估结果：后端处理完毕后给出的反馈 ---
class EvaluationOut(BaseModel):
    id: int
    total_value: float = Field(..., description="9类指标直接相加后的总评估价值")
    status: str
    created_at: datetime

    class Config:
        from_attributes = True # 允许从 SQLAlchemy 模型对象直接转换

# --- 4. 用户基础模块：用于信息展示 ---
class UserBase(BaseModel):
    username: str
    hospital: Optional[str] = None

# --- 5. 专门用于用户注册：包含密码校验 ---
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="用户注册密码，不得少于6位")

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True