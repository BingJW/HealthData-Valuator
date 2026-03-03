from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#修改1
from app.core.database import engine
from app.models import models

#修改2
# 导入API 路由
from app.api.api import router as api_router

#修改3
# 自动创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HealthData-Valuator API", version="1.0.0")

# 配置 CORS 中间件，允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载指标测算接口
app.include_router(api_router, prefix="")

@app.get("/")
async def root():
    return {"status": "running", 
            "project": "HealthData-Valuator API",
            "message":"后端接口已就绪"
    }
