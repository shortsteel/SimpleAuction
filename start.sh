#!/bin/bash

# 简单拍卖系统启动脚本

echo "=========================================="
echo "  简单拍卖系统 - 启动脚本"
echo "=========================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查npm是否安装
if ! command -v npm &> /dev/null; then
    echo "错误: 未找到 npm，请先安装 npm"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 启动后端
echo "正在启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
if [ ! -f ".deps_installed" ]; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# 启动后端（后台运行）
echo "启动后端服务 (http://localhost:3000)..."
python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID)"
cd ..

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

# 启动前端
echo ""
echo "正在启动前端服务..."
cd frontend

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端（后台运行）
echo "启动前端服务 (http://localhost:8080)..."
npm run serve > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动 (PID: $FRONTEND_PID)"
cd ..

# 保存PID到文件
echo $BACKEND_PID > backend.pid
echo $FRONTEND_PID > frontend.pid

echo ""
echo "=========================================="
echo "  服务启动完成！"
echo "=========================================="
echo "后端服务: http://localhost:3000"
echo "前端服务: http://localhost:8080"
echo ""
echo "后端日志: backend.log"
echo "前端日志: frontend.log"
echo ""
echo "停止服务: ./stop.sh"
echo "或手动停止: kill $BACKEND_PID $FRONTEND_PID"
echo "=========================================="

