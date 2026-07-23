@echo off
chcp 65001 >nul
title AI Novel Frontend
echo ============================================
echo   AI Novel - 前端开发服务器
echo ============================================
echo.

cd /d d:\deellearn\dev2\vue-project

:: 检查 node_modules 是否存在
if not exist "node_modules" (
    echo [提示] 首次运行，正在安装依赖...
    call npm install
)

echo [启动] 正在启动 Vue 开发服务器...
echo [地址] http://localhost:5173/novel
echo [提示] 按 Ctrl+C 停止服务
echo.

npm run dev
