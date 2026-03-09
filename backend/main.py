# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import secrets
import uvicorn

# --- 数据模拟存储 ---
evaluations_db = {}
evaluation_counter = 1
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "password123",
        "hospital": "北京协和医院",
        "phone": "13800138000",
        "email": "test@example.com"
    }
}

# 阶段四新增：模拟系统权重配置
system_weights = {
    "strategic_weight": 0.3,
    "security_weight": 0.4,
    "usability_weight": 0.3,
    "last_updated": datetime.now().isoformat()
}

# --- Pydantic 模型（用于数据验证） ---
class WeightUpdate(BaseModel):
    strategic_weight: float
    security_weight: float
    usability_weight: float

# --- 应用初始化 ---
app = FastAPI(title="HealthData-Valuator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 辅助函数 ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return secrets.token_urlsafe(32)

# --- 基础接口 ---
@app.get("/")
async def root():
    return {
        "status": "running", 
        "project": "HealthData-Valuator API",
        "version": "1.0.0",
        "message": "后端服务运行正常"
    }

# --- 认证模块 ---
@app.post("/api/auth/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")
    if username not in fake_users_db or password != fake_users_db[username]["password"]:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = create_access_token(data={"sub": username})
    return {
        "code": 0,
        "message": "登录成功",
        "data": {"token": token, "user_info": fake_users_db[username]}
    }

@app.post("/api/auth/register")
async def register(data: dict):
    username = data.get("username")
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    fake_users_db[username] = data
    return {"code": 0, "message": "注册成功", "data": {"username": username}}

# --- 评估模块 ---
@app.post("/api/evaluations")
async def create_evaluation(data: dict):
    global evaluation_counter
    evaluation_id = str(evaluation_counter)
    evaluation_counter += 1

    indicators = data.get("indicators", [])
    total_value = sum(item.get("amount", 0) for item in indicators)

    evaluations_db[evaluation_id] = {
        "id": evaluation_id,
        "name": data.get("name", f"评估{evaluation_id}"),
        "indicators": indicators,
        "total_value": total_value,
        "created_at": datetime.now().isoformat(),
        "status": "completed"
    }
    return {"code": 0, "message": "评估创建成功", "data": {"id": evaluation_id, "total_value": total_value}}

# --- 阶段四：管理员看板接口 (Admin Stats) ---
@app.get("/api/admin/stats")
async def get_admin_stats():
    """
    全量数据汇总：前端管理员面板调用
    """
    all_evals = list(evaluations_db.values())
    total_value = sum(e["total_value"] for e in all_evals)
    count = len(all_evals)
    avg_value = total_value / count if count > 0 else 0

    return {
        "code": 0,
        "message": "全量统计获取成功",
        "data": {
            "total_evaluations": count,
            "total_market_value": round(total_value, 2),
            "average_value": round(avg_value, 2),
            "total_users": len(fake_users_db),
            "system_health": "excellent"
        }
    }

# --- 阶段四：动态权重调整接口 (Admin Weights) ---
@app.put("/api/admin/weights")
async def update_weights(weights: WeightUpdate):
    """
    更新全局权重系数：前端权重设置页面调用
    """
    global system_weights
    system_weights.update({
        "strategic_weight": weights.strategic_weight,
        "security_weight": weights.security_weight,
        "usability_weight": weights.usability_weight,
        "last_updated": datetime.now().isoformat()
    })
    return {
        "code": 0,
        "message": "全局权重系数已更新",
        "data": system_weights
    }

@app.get("/api/admin/weights")
async def get_weights():
    """获取当前权重配置"""
    return {"code": 0, "data": system_weights}

# --- 演示数据初始化 ---
@app.post("/api/demo/init")
async def init_demo_data():
    # ... (保持你原有代码的初始化逻辑不变)
    evaluations_db.clear()
    # 示例数据
    evaluations_db["1"] = {"id": "1", "name": "演示数据", "total_value": 170000.0, "created_at": datetime.now().isoformat()}
    return {"code": 0, "message": "演示数据已重置"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)