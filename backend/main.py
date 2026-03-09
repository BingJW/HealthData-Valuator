# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import secrets
import uvicorn
import json

# 引入 SQLAlchemy 相关库
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- 1. 数据库配置（持久化到本地文件 sql_app.db） ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. 数据库模型定义 ---
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # 实际项目建议 hash 加密
    hospital = Column(String)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

class EvaluationTable(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    total_value = Column(Float, default=0.0)
    indicators = Column(String)  
    created_at = Column(String)
    status = Column(String, default="completed")

# 创建数据库表（如果不存在）
Base.metadata.create_all(bind=engine)

# --- 3. Pydantic 模型（请求体校验） ---
class UserRegister(BaseModel):
    username: str
    password: str
    hospital: str
    phone: Optional[str] = ""
    email: Optional[str] = ""

class UserLogin(BaseModel):
    username: str
    password: str

class WeightUpdate(BaseModel):
    strategic_weight: float
    security_weight: float
    usability_weight: float

# --- 4. 依赖项 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. 应用初始化 ---
app = FastAPI(title="HealthData-Valuator API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 辅助函数：生成 Token
def create_access_token(data: dict):
    return secrets.token_urlsafe(32)

# --- 6. 接口实现 ---

@app.get("/")
async def root():
    return {"status": "online", "message": "数据库持久化已开启"}

# 【注册】将用户信息永久存入 SQLite
@app.post("/api/auth/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(UserTable).filter(UserTable.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    new_user = UserTable(
        username=user_data.username,
        password=user_data.password,
        hospital=user_data.hospital,
        phone=user_data.phone,
        email=user_data.email
    )
    db.add(new_user)
    db.commit()
    return {"code": 0, "message": "注册成功，账号已安全存入数据库"}

# 【登录】从数据库验证身份
@app.post("/api/auth/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.username == credentials.username).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = create_access_token({"sub": user.username})
    return {
        "code": 0,
        "data": {
            "token": token,
            "user_info": {"username": user.username, "hospital": user.hospital}
        }
    }

# 【评估】创建评估记录
@app.post("/api/evaluations")
async def create_evaluation(data: dict, db: Session = Depends(get_db)):
    try:
        raw_indicators = data.get("indicators", [])
        
        total_val = 0.0
        for item in raw_indicators:
            total_val += float(item.get("amount", 0))

        new_eval = EvaluationTable(
            name=data.get("evaluation_name", "未命名评估"),
            description=data.get("description", ""),
            total_value=total_val,
            indicators=json.dumps(raw_indicators), # 转为纯文本字符串
            created_at=datetime.now().isoformat()
        )
        db.add(new_eval)
        db.commit()
        db.refresh(new_eval)
        return {"code": 0, "data": {"id": new_eval.id, "total_value": total_val}}
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
# --- 阶段四：管理员看板接口 ---
@app.get("/api/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    # 从数据库实时计算汇总
    total_val = db.query(func.sum(EvaluationTable.total_value)).scalar() or 0
    total_count = db.query(func.count(EvaluationTable.id)).scalar() or 0
    avg_val = total_val / total_count if total_count > 0 else 0
    user_count = db.query(func.count(UserTable.id)).scalar() or 0

    return {
        "code": 0,
        "data": {
            "total_evaluations": total_count,
            "total_market_value": round(total_val, 2),
            "average_value": round(avg_val, 2),
            "total_users": user_count
        }
    }

@app.put("/api/admin/weights")
async def update_weights(weights: WeightUpdate):
    # 这里演示权重更新，实际可存入新的 config 表
    return {"code": 0, "message": "权重已更新", "data": weights}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)