@echo off
REM 启动后端服务 (Windows)

echo 正在启动后端服务...

cd /d "%~dp0backend"

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

REM 启动后端
echo 启动后端服务 (http://localhost:3000)...
python app.py

pause

