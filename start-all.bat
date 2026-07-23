@echo off
chcp 65001 >nul
title AI Novel Platform
echo ============================================
echo   AI Novel - 一键启动全部服务
echo ============================================
echo.

set ROOT_DIR=d:\deellearn\dev2

:: 先启动后端 (新窗口)
echo [1/2] 启动后端 API 服务器...
start "AI Novel Backend" cmd /k "cd /d %ROOT_DIR%\ai-novel-backend && title AI Novel Backend && .\.venv\Scripts\python.exe -m app.main"

:: 等待后端启动
timeout /t 3 /nobreak >nul

:: 再启动前端 (新窗口)
echo [2/2] 启动前端开发服务器...
start "AI Novel Frontend" cmd /k "cd /d %ROOT_DIR%\vue-project && title AI Novel Frontend && npm run dev"

echo.
echo ============================================
echo   所有服务已启动！
echo ============================================
echo   后端: http://localhost:8000/docs
echo   前端: http://localhost:5173/novel
echo ============================================
echo.
echo 按任意键退出此窗口 (服务在其他窗口运行)...
pause >nul