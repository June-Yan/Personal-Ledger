from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.config import get_settings
from app.routers import auth, categories, bills, reports
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 数据库表创建完成")
except Exception as e:
    logger.error(f"❌ 数据库初始化失败: {e}")
    raise

app = FastAPI(title="个人记账本 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"code": 50001, "message": str(exc) or "服务器内部错误", "data": None}
    )


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(bills.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "个人记账本 API 服务运行中"}
