# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
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

# --- 1. 数据库配置（MySQL） ---
# 注意：main.py 中的数据库配置已迁移到 app/core/database.py
# 这里保留是为了向后兼容，建议使用 app/core/database.py 中的配置
from app.core.database import engine, SessionLocal, Base
from app.core.config import get_database_url
SQLALCHEMY_DATABASE_URL = get_database_url()

# --- 2. 数据库模型定义 ---
class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))  # 实际项目建议 hash 加密
    hospital = Column(String(200))
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

class EvaluationTable(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(String(500), nullable=True)
    total_value = Column(Float, default=0.0)
    indicators = Column(String(5000))
    created_at = Column(String(50))
    status = Column(String(50), default="completed")
    username = Column(String(50), nullable=True, index=True)  # 创建者，用于「我的评估」仅看本人

# 创建数据库表（如果不存在）
# 注意：表结构定义在 app/models/models.py 中
# 首次运行前请确保 MySQL 数据库已创建，然后运行: python init_db.py
# 或者直接启动应用，表会自动创建
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"警告: 数据库表创建失败，请检查数据库连接配置: {e}")

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


class AdminUserCreate(BaseModel):
    username: str
    password: str
    hospital: str = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""


class AdminUserUpdate(BaseModel):
    hospital: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

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
    # token 保存在 localStorage，并非 cookie 跨站，不需要凭证模式
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 辅助函数：生成 Token；内存存储 token -> username 供 /api/user/info 校验
_token_store = {}

def create_access_token(data: dict):
    return secrets.token_urlsafe(32)

def get_current_username(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")
    token = authorization[7:]
    username = _token_store.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="登录已过期")
    return username


def require_admin(username: str = Depends(get_current_username)) -> str:
    if username != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return username


# --- 6. 接口实现 ---

@app.get("/")
async def root():
    return {"status": "online", "message": "MySQL 数据库连接已启用"}

# 【注册】将用户信息永久存入 MySQL
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
    try:
        user = db.query(UserTable).filter(UserTable.username == credentials.username).first()
        if not user or user.password != credentials.password:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        token = create_access_token({"sub": user.username})
        _token_store[token] = user.username
        return {
            "code": 0,
            "data": {
                "token": token,
                "user_info": {
                    "username": user.username,
                    "hospital": user.hospital or "",
                    "phone": user.phone or "",
                    "email": user.email or ""
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@app.post("/api/auth/logout")
async def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        _token_store.pop(token, None)
    return {"code": 0, "message": "已退出登录"}

@app.get("/api/user/info")
async def get_user_info(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    user = db.query(UserTable).filter(UserTable.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "code": 0,
        "data": {
            "username": user.username,
            "hospital": user.hospital,
            "phone": user.phone or "",
            "email": user.email or ""
        }
    }

# 9大类成本名称，用于结果页
INDICATOR_CATEGORY_NAMES = {
    1: "数据战略与治理成本", 2: "数据获取与采集成本", 3: "数据存储与备份成本",
    4: "数据处理与加工成本", 5: "数据应用与分析成本", 6: "数据流通与共享成本",
    7: "数据安全、隐私与合规成本", 8: "数据归档与销毁成本", 9: "数据全流程人力成本"
}

@app.get("/api/indicators")
async def get_indicators():
    """返回指标分类与项（供前端表单项使用）"""
    categories = [
        {"id": i, "name": INDICATOR_CATEGORY_NAMES[i]} for i in range(1, 10)
    ]
    return {"code": 0, "data": {"categories": categories}}

@app.post("/api/evaluations")
async def create_evaluation(data: dict, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    try:
        raw_indicators = data.get("indicators", [])
        total_val = 0.0
        for item in raw_indicators:
            total_val += float(item.get("amount", 0))
        name = data.get("name") or data.get("evaluation_name") or "未命名评估"
        new_eval = EvaluationTable(
            name=name,
            description=data.get("description", ""),
            total_value=total_val,
            indicators=json.dumps(raw_indicators, ensure_ascii=False),
            created_at=datetime.now().isoformat(),
            username=username
        )
        db.add(new_eval)
        db.commit()
        db.refresh(new_eval)
        return {"code": 0, "data": {"id": new_eval.id, "total_value": total_val}}
    except Exception as e:
        err_msg = str(e)
        if "username" in err_msg.lower() and ("unknown column" in err_msg.lower() or "no such column" in err_msg.lower()):
            raise HTTPException(
                status_code=500,
                detail="数据库缺少 username 列，请在 MySQL 中执行：ALTER TABLE evaluations ADD COLUMN username VARCHAR(50) NULL DEFAULT NULL;"
            )
        raise HTTPException(status_code=500, detail=err_msg)

@app.get("/api/evaluations/stats")
async def get_evaluation_stats(db: Session = Depends(get_db)):
    total_val = db.query(func.sum(EvaluationTable.total_value)).scalar() or 0
    total_count = db.query(func.count(EvaluationTable.id)).scalar() or 0
    avg_val = total_val / total_count if total_count else 0
    return {"code": 0, "data": {"total_count": total_count, "total_value": round(float(total_val), 2), "average_value": round(float(avg_val), 2)}}

@app.get("/api/evaluations")
async def list_evaluations(
    page: int = 1, pageSize: int = 10, status: Optional[str] = None,
    keyword: Optional[str] = None, db: Session = Depends(get_db), username: str = Depends(get_current_username)
):
    try:
        q = db.query(EvaluationTable)
        if username != "admin":
            q = q.filter(EvaluationTable.username == username)
        if keyword:
            q = q.filter(EvaluationTable.name.contains(keyword))
        if status and status != "all":
            q = q.filter(EvaluationTable.status == status)
        total = q.count()
        items = q.order_by(EvaluationTable.created_at.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
        return {
            "code": 0,
            "data": {
                "list": [
                    {"id": e.id, "name": e.name, "description": e.description, "totalValue": e.total_value,
                     "createdAt": e.created_at, "status": e.status or "completed"}
                    for e in items
                ],
                "total": total
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取评估列表失败: {str(e)}")

@app.get("/api/evaluations/{eval_id}")
async def get_evaluation(eval_id: int, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    return {"code": 0, "data": {"id": e.id, "name": e.name, "description": e.description, "totalValue": e.total_value, "createdAt": e.created_at, "status": e.status, "indicators": json.loads(e.indicators) if isinstance(e.indicators, str) else (e.indicators or [])}}

def _build_result_from_eval(e):
    raw = json.loads(e.indicators) if isinstance(e.indicators, str) else (e.indicators or [])
    total_val = float(e.total_value)
    by_cat = {}
    details = []
    for item in raw:
        cat_id = item.get("category", 1)
        cat_name = INDICATOR_CATEGORY_NAMES.get(cat_id, "其他")
        amt = float(item.get("amount", 0))
        by_cat[cat_id] = by_cat.get(cat_id, 0) + amt
        details.append({
            "categoryId": cat_id,
            "categoryName": cat_name,
            "itemName": item.get("item_name", ""),
            "amount": amt,
            "percentage": round((amt / total_val * 100), 2) if total_val else 0,
            "description": ""
        })
    categories = [{"id": k, "name": INDICATOR_CATEGORY_NAMES.get(k, "其他"), "value": v} for k, v in sorted(by_cat.items())]
    return {
        "reportId": f"REPORT-{e.id}-{int(datetime.now().timestamp())}",
        "hospital": "",
        "createdAt": e.created_at,
        "name": e.name,
        "status": e.status or "completed",
        "totalValue": total_val,
        "categories": categories,
        "details": details
    }

@app.get("/api/evaluations/{eval_id}/result")
async def get_evaluation_result(eval_id: int, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    result = _build_result_from_eval(e)
    return {"code": 0, "data": result}

@app.put("/api/evaluations/{eval_id}")
async def update_evaluation(eval_id: int, data: dict, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    raw_indicators = data.get("indicators")
    if raw_indicators is None:
        raw_indicators = json.loads(e.indicators) if isinstance(e.indicators, str) else (e.indicators or [])
    total_val = sum(float(i.get("amount", 0)) for i in raw_indicators)
    e.name = data.get("name", e.name)
    e.description = data.get("description", e.description)
    e.total_value = total_val
    e.indicators = json.dumps(raw_indicators, ensure_ascii=False)
    db.commit()
    db.refresh(e)
    return {"code": 0, "data": {"id": e.id, "total_value": e.total_value}}

@app.delete("/api/evaluations/{eval_id}")
async def delete_evaluation(eval_id: int, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    db.delete(e)
    db.commit()
    return {"code": 0, "message": "删除成功"}

@app.post("/api/evaluations/{eval_id}/submit")
async def submit_evaluation(eval_id: int, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    e.status = "completed"
    db.commit()
    return {"code": 0, "data": {"id": e.id}}

@app.post("/api/evaluations/{eval_id}/duplicate")
async def duplicate_evaluation(eval_id: int, db: Session = Depends(get_db)):
    e = db.query(EvaluationTable).filter(EvaluationTable.id == eval_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="评估不存在")
    raw = json.loads(e.indicators) if isinstance(e.indicators, str) else (e.indicators or [])
    new_eval = EvaluationTable(
        name=e.name + " (副本)",
        description=e.description,
        total_value=e.total_value,
        indicators=e.indicators,
        created_at=datetime.now().isoformat(),
        status="completed"
    )
    db.add(new_eval)
    db.commit()
    db.refresh(new_eval)
    return {"code": 0, "data": {"id": new_eval.id}}

# --- 阶段四：管理员看板接口 ---
@app.get("/api/admin/users")
async def list_users(
    page: int = 1, pageSize: int = 20, keyword: Optional[str] = None,
    db: Session = Depends(get_db), _: str = Depends(require_admin)
):
    q = db.query(UserTable)
    if keyword:
        q = q.filter(UserTable.username.contains(keyword) | UserTable.hospital.contains(keyword))
    total = q.count()
    items = q.order_by(UserTable.id.desc()).offset((page - 1) * pageSize).limit(pageSize).all()
    return {
        "code": 0,
        "data": {
            "list": [{"id": u.id, "username": u.username, "hospital": u.hospital or "", "phone": u.phone or "", "email": u.email or ""} for u in items],
            "total": total
        }
    }


@app.post("/api/admin/users")
async def admin_create_user(body: AdminUserCreate, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    if db.query(UserTable).filter(UserTable.username == body.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    u = UserTable(
        username=body.username.strip(),
        password=body.password,
        hospital=body.hospital or "",
        phone=body.phone or "",
        email=body.email or ""
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"code": 0, "data": {"id": u.id, "username": u.username, "hospital": u.hospital or "", "phone": u.phone or "", "email": u.email or ""}}


@app.get("/api/admin/users/{user_id}")
async def admin_get_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    u = db.query(UserTable).filter(UserTable.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 0, "data": {"id": u.id, "username": u.username, "hospital": u.hospital or "", "phone": u.phone or "", "email": u.email or ""}}


@app.put("/api/admin/users/{user_id}")
async def admin_update_user(user_id: int, body: AdminUserUpdate, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    u = db.query(UserTable).filter(UserTable.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="用户不存在")
    if body.hospital is not None:
        u.hospital = body.hospital
    if body.phone is not None:
        u.phone = body.phone
    if body.email is not None:
        u.email = body.email
    if body.password is not None and body.password.strip() != "":
        u.password = body.password
    db.commit()
    db.refresh(u)
    return {"code": 0, "data": {"id": u.id, "username": u.username, "hospital": u.hospital or "", "phone": u.phone or "", "email": u.email or ""}}


@app.delete("/api/admin/users/{user_id}")
async def admin_delete_user(user_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    u = db.query(UserTable).filter(UserTable.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="用户不存在")
    if u.username == "admin":
        raise HTTPException(status_code=400, detail="不能删除管理员账号")
    db.delete(u)
    db.commit()
    return {"code": 0, "message": "已删除"}

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
            "total_value": round(total_val, 2),
            "average_value": round(avg_val, 2),
            "total_users": user_count
        }
    }

_default_weights = {str(i): 1.0 for i in range(1, 10)}

@app.get("/api/admin/weights")
async def get_weights():
    return {"code": 0, "data": _default_weights}

@app.put("/api/admin/weights")
async def update_weights(weights: dict):
    for k, v in (weights or {}).items():
        if str(k) in _default_weights:
            _default_weights[str(k)] = float(v)
    return {"code": 0, "message": "权重已更新", "data": _default_weights}

@app.post("/api/demo/init")
async def init_demo_data(db: Session = Depends(get_db)):
    """初始化演示数据：创建测试用户与示例评估（若已存在则跳过）"""
    demo_users = [
        ("admin", "admin123", "系统演示医院", "13800000001", "admin@demo.com"),
        ("doctor_zhang", "password123", "北京协和医院", "13800000002", "zhang@demo.com"),
        ("nurse_li", "password123", "上海瑞金医院", "13800000003", "li@demo.com"),
    ]
    for username, password, hospital, phone, email in demo_users:
        if db.query(UserTable).filter(UserTable.username == username).first():
            continue
        db.add(UserTable(username=username, password=password, hospital=hospital, phone=phone, email=email))
    db.commit()
    demo_evals = [
        ("2023年度数据资产评估", 1250000, [{"category": 1, "item_name": "plan", "amount": 1250000}]),
        ("急诊科数据专项评估", 850000, [{"category": 2, "item_name": "collect", "amount": 850000}]),
        ("医疗影像数据评估", 2100000, [{"category": 3, "item_name": "storage", "amount": 2100000}]),
    ]
    for name, total, ind in demo_evals:
        db.add(EvaluationTable(
            name=name, description="演示数据", total_value=total,
            indicators=json.dumps(ind, ensure_ascii=False),
            created_at=datetime.now().isoformat()
        ))
    db.commit()
    return {"code": 0, "message": "演示数据初始化成功"}

@app.put("/api/user/info")
async def update_user_info(data: dict, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    user = db.query(UserTable).filter(UserTable.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if "hospital" in data:
        user.hospital = data["hospital"]
    if "phone" in data:
        user.phone = data["phone"]
    if "email" in data:
        user.email = data["email"]
    db.commit()
    db.refresh(user)
    return {"code": 0, "data": {"username": user.username, "hospital": user.hospital, "phone": user.phone or "", "email": user.email or ""}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)