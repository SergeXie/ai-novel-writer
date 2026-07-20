@echo off
chcp 65001 >nul
echo ============================================
echo   AI Novel - 前端开发服务器
echo ============================================
echo.

cd /d d:\deellearn\dev2\vue-project

echo [启动] 正在启动 Vue 开发服务器...
echo [地址] http://localhost:5173/novel
echo.

npm run dev
