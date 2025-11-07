#!/bin/bash

# 启动前端服务

echo "正在启动前端服务..."

cd "$(dirname "$0")/frontend"

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端
echo "启动前端服务 (http://localhost:8080)..."
npm run serve

