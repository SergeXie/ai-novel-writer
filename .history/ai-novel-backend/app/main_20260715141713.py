"""
AI Novel Backend - 主应用入口
企业级 FastAPI 应用
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.logging import setup_logging
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.context import RequestContextMiddleware
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    启动时初始化资源，关闭时清理资源
    """
    # ---- 启动阶段 ----
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")

    # 初始化日志
    setup_logging()

    # 初始化数据库
    await init_db()
    logger.info("✅ 数据库初始化完成")

    # 创建日志目录
    import os
    os.makedirs("logs", exist_ok=True)

    logger.info(f"✅ {settings.APP_NAME} 启动完成")
    logger.info(f"📖 API 文档: http://{settings.HOST}:{settings.PORT}/docs")

    yield  # 应用运行中

    # ---- 关闭阶段 ----
    logger.info("🛑 正在关闭应用...")
    await close_db()
    logger.info("✅ 资源清理完成")


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI 驱动的小说创作后端服务",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ---- 中间件配置 ----
    # CORS 跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 请求日志
    app.add_middleware(RequestLoggingMiddleware)

    # 请求上下文
    app.add_middleware(RequestContextMiddleware)

    # ---- 路由注册 ----
    app.include_router(api_router)

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
