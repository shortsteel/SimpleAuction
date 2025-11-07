@echo off
REM 简单拍卖系统启动脚本 (Windows)

echo ==========================================
echo   简单拍卖系统 - 启动脚本
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)

REM 检查npm是否安装
npm --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 npm，请先安装 npm
    pause
    exit /b 1
)

REM 获取脚本所在目录
cd /d "%~dp0"

REM 启动后端
echo 正在启动后端服务...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
if not exist ".deps_installed" (
    echo 安装Python依赖...
    pip install -r requirements.txt
    echo. > .deps_installed
)

REM 启动后端（新窗口）
echo 启动后端服务 (http://localhost:3000)...
start "后端服务" cmd /k "python app.py"
cd ..

REM 等待后端启动
echo 等待后端服务启动...
timeout /t 3 /nobreak >nul

REM 启动前端
echo.
echo 正在启动前端服务...
cd frontend

REM 检查node_modules
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

REM 启动前端（新窗口）
echo 启动前端服务 (http://localhost:8080)...
start "前端服务" cmd /k "npm run serve"
cd ..

echo.
echo ==========================================
echo   服务启动完成！
echo ==========================================
echo 后端服务: http://localhost:3000
echo 前端服务: http://localhost:8080
echo.
echo 关闭服务: 关闭对应的命令行窗口
echo ==========================================
pause

