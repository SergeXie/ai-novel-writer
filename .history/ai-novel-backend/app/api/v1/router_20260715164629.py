"""
API v1 路由聚合
"""
from fastapi import APIRouter
from app.api.v1 import auth, novels, chat, system, snippets

# 聚合所有 v1 路由
api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(novels.router)
api_router.include_router(chat.router)
api_router.include_router(system.router)
api_router.include_router(snippets.router)
