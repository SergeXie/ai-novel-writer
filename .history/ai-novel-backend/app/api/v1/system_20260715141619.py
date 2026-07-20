"""
健康检查 API
"""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["系统"])


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/info")
async def app_info():
    """应用信息"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "environment": settings.ENVIRONMENT,
        "default_model": settings.DEFAULT_MODEL,
    }
