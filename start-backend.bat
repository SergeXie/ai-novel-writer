@echo off
chcp 65001 >nul
title AI Novel Backend
echo ============================================
echo   AI Novel - 后端 API 服务器
echo ============================================
echo.

set PROJECT_DIR=d:\deellearn\dev2\ai-novel-backend
cd /d "%PROJECT_DIR%"

:: 检查虚拟环境是否存在
if not exist ".\.venv\Scripts\python.exe" (
    echo [错误] 未找到 Python 虚拟环境!
    echo [提示] 请先运行: python -m venv .venv
    echo.
    pause
    exit /b 1
)

:: 确保 data 目录存在
if not exist "data" mkdir data

:: 杀掉可能残留的旧后端进程 (端口 8000)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo [清理] 停止占用端口 8000 的进程 (PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
)

echo [启动] 正在启动 FastAPI 后端服务...
echo [地址] http://localhost:8000
echo [文档] http://localhost:8000/docs
echo [提示] 按 Ctrl+C 停止服务
echo.

.\.venv\Scripts\python.exe -m app.main
