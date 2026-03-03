from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#修改1
from app.core.database import engine, Base
from app.models import models

app = FastAPI(title="HealthData-Valuator API", version="1.0.0")

#修改2
models.Base.metadata.create_all(bind=engine)

# 配置 CORS 中间件，允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "running", "project": "HealthData-Valuator API"}
