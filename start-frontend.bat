@echo off
REM 启动前端服务 (Windows)

echo 正在启动前端服务...

cd /d "%~dp0frontend"

REM 检查node_modules
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

REM 启动前端
echo 启动前端服务 (http://localhost:8080)...
npm run serve

pause

