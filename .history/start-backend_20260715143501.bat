@echo off
chcp 65001 >nul
echo ============================================
echo   AI Novel - 后端 API 服务器
echo ============================================
echo.

cd /d d:\deellearn\dev2\ai-novel-backend

echo [启动] 正在启动 FastAPI 后端服务...
echo [地址] http://localhost:8000
echo [文档] http://localhost:8000/docs
echo.

.\.venv\Scripts\python.exe -m app.main
