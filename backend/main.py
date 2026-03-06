# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import secrets
import uvicorn

# 模拟评估数据存储
evaluations_db = {}
evaluation_counter = 1

# 创建 FastAPI 应用实例
app = FastAPI(title="HealthData-Valuator API", version="1.0.0")

# 配置 CORS 中间件，允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟用户数据库
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "password123",
        "hospital": "北京协和医院",
        "phone": "13800138000",
        "email": "test@example.com"
    }
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token = secrets.token_urlsafe(32)
    return token

@app.get("/")
async def root():
    """根路径，返回API状态"""
    return {
        "status": "running", 
        "project": "HealthData-Valuator API",
        "version": "1.0.0",
        "message": "后端服务运行正常"
    }

# 注意：这里添加了 /api 前缀
@app.post("/api/auth/login")
async def login(data: dict):
    """用户登录接口"""
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")
    
    # 检查用户是否存在
    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    user = fake_users_db[username]
    
    # 检查密码
    if password != user["password"]:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 生成访问令牌
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "code": 0,
        "message": "登录成功",
        "data": {
            "token": access_token,
            "user_info": {
                "username": user["username"],
                "hospital": user["hospital"],
                "phone": user["phone"],
                "email": user["email"]
            }
        }
    }

# 注意：这里添加了 /api 前缀
@app.post("/api/auth/register")
async def register(data: dict):
    """用户注册接口"""
    username = data.get("username")
    password = data.get("password")
    hospital = data.get("hospital")
    phone = data.get("phone", "")
    email = data.get("email", "")
    
    if not username or not password or not hospital:
        raise HTTPException(status_code=400, detail="用户名、密码和医院名称不能为空")
    
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    fake_users_db[username] = {
        "username": username,
        "password": password,
        "hospital": hospital,
        "phone": phone,
        "email": email
    }
    
    return {
        "code": 0,
        "message": "注册成功",
        "data": {
            "username": username,
            "hospital": hospital
        }
    }

# 注意：这里添加了 /api 前缀
@app.get("/api/user/info")
async def get_user_info():
    """获取用户信息"""
    # 这里简化处理，实际应从token解析用户信息
    return {
        "code": 0,
        "message": "获取用户信息成功",
        "data": {
            "username": "testuser",
            "hospital": "北京协和医院",
            "phone": "13800138000",
            "email": "test@example.com"
        }
    }

# 注意：这里添加了 /api 前缀
@app.post("/api/auth/logout")
async def logout():
    """用户退出登录"""
    return {
        "code": 0,
        "message": "退出登录成功"
    }

@app.post("/api/evaluations")
async def create_evaluation(data: dict):
    """
    创建新的评估接口
    接收前端传来的评估名称、描述和指标数据列表
    """
    global evaluation_counter  # 引用全局计数器

    # 生成一个模拟的评估ID
    evaluation_id = str(evaluation_counter)
    evaluation_counter += 1  # 为下一次创建递增

    # 提取并计算总价值（直接相加）
    indicators = data.get("indicators", [])
    total_value = sum(item.get("amount", 0) for item in indicators)

    # 将评估数据存储到模拟的数据库中
    evaluations_db[evaluation_id] = {
        "id": evaluation_id,
        "name": data.get("name", f"评估{evaluation_id}"),
        "description": data.get("description", ""),
        "indicators": indicators,
        "total_value": total_value,
        "created_at": datetime.now().isoformat(),
        "status": "completed"
    }

    # 返回成功响应，包含新创建的评估ID
    return {
        "code": 0,
        "message": "评估创建成功",
        "data": {
            "id": evaluation_id,
            "name": evaluations_db[evaluation_id]["name"],
            "total_value": total_value
        }
    }

# backend/main.py
@app.post("/api/demo/init")
async def init_demo_data():
    """初始化演示数据"""
    # 清空现有数据
    fake_users_db.clear()
    evaluations_db.clear()
    
    # 初始化测试用户
    demo_users = [
        {
            "username": "admin",
            "password": "admin123",
            "hospital": "北京协和医院",
            "phone": "13800138001",
            "email": "admin@example.com"
        },
        {
            "username": "doctor_zhang",
            "password": "password123",
            "hospital": "上海瑞金医院",
            "phone": "13800138002",
            "email": "zhang@example.com"
        },
        {
            "username": "nurse_li",
            "password": "password123",
            "hospital": "广州中山医院",
            "phone": "13800138003",
            "email": "li@example.com"
        }
    ]
    
    for user in demo_users:
        fake_users_db[user["username"]] = user
    
    # 初始化演示评估数据
    demo_evaluations = [
        {
            "id": "1",
            "name": "2023年度数据资产评估",
            "description": "年度全面数据资产评估报告",
            "total_value": 1250000.00,
            "indicators": [
                {"category": 1, "item_name": "strategicPlanning", "amount": 50000},
                {"category": 1, "item_name": "governanceSystem", "amount": 80000},
                {"category": 2, "item_name": "hardwareCollection", "amount": 150000},
                {"category": 3, "item_name": "storageHardware", "amount": 120000},
                {"category": 4, "item_name": "dataCleaning", "amount": 90000},
                {"category": 5, "item_name": "businessApplication", "amount": 300000},
                {"category": 6, "item_name": "dataExchange", "amount": 60000},
                {"category": 7, "item_name": "securityHardware", "amount": 80000},
                {"category": 8, "item_name": "archivingSystem", "amount": 40000},
                {"category": 9, "item_name": "strategyGovernance", "amount": 280000}
            ],
            "created_at": "2023-12-15T10:30:00",
            "status": "completed"
        },
        {
            "id": "2",
            "name": "急诊科数据专项评估",
            "description": "急诊科业务数据价值评估",
            "total_value": 850000.00,
            "indicators": [
                {"category": 2, "item_name": "dataPurchase", "amount": 200000},
                {"category": 3, "item_name": "cloudStorage", "amount": 120000},
                {"category": 5, "item_name": "analyticsModeling", "amount": 180000},
                {"category": 7, "item_name": "privacyProtection", "amount": 100000},
                {"category": 9, "item_name": "technicalOperations", "amount": 250000}
            ],
            "created_at": "2023-11-20T14:15:00",
            "status": "completed"
        },
        {
            "id": "3",
            "name": "医疗影像数据评估",
            "description": "PACS系统影像数据价值分析",
            "total_value": 2100000.00,
            "indicators": [
                {"category": 2, "item_name": "hardwareCollection", "amount": 500000},
                {"category": 3, "item_name": "storageHardware", "amount": 300000},
                {"category": 3, "item_name": "backupDisaster", "amount": 200000},
                {"category": 4, "item_name": "dataProcessing", "amount": 400000},
                {"category": 5, "item_name": "visualization", "amount": 300000},
                {"category": 9, "item_name": "dataAnalysis", "amount": 400000}
            ],
            "created_at": "2023-10-10T09:45:00",
            "status": "completed"
        }
    ]
    
    for eval in demo_evaluations:
        evaluations_db[eval["id"]] = eval
    
    return {
        "code": 0,
        "message": "演示数据初始化成功",
        "data": {
            "users_created": len(demo_users),
            "evaluations_created": len(demo_evaluations)
        }
    }

@app.get("/api/demo/stats")
async def get_demo_stats():
    """获取演示统计数据"""
    total_value = sum(eval["total_value"] for eval in evaluations_db.values())
    avg_value = total_value / len(evaluations_db) if evaluations_db else 0
    
    return {
        "code": 0,
        "message": "获取统计数据成功",
        "data": {
            "total_evaluations": len(evaluations_db),
            "total_users": len(fake_users_db),
            "total_value": total_value,
            "average_value": avg_value,
            "last_updated": datetime.now().isoformat()
        }
    }

# 如果直接运行此文件
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)