#!/bin/bash

# 启动后端服务

echo "正在启动后端服务..."

cd "$(dirname "$0")/backend"

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

# 启动后端
echo "启动后端服务 (http://localhost:3000)..."
python app.py

