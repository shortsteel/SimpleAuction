#!/bin/bash

# 简单拍卖系统停止脚本

echo "正在停止服务..."

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 停止后端
if [ -f "backend.pid" ]; then
    BACKEND_PID=$(cat backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "停止后端服务 (PID: $BACKEND_PID)..."
        # 先尝试优雅停止
        kill $BACKEND_PID 2>/dev/null
        sleep 1
        # 如果进程还在，强制停止
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID 2>/dev/null
        fi
        rm backend.pid
    else
        echo "后端服务未运行"
        rm backend.pid
    fi
fi

# 通过端口查找并停止所有相关进程（包括 Flask reloader 的父进程）
BACKEND_PIDS=$(lsof -ti:3000 2>/dev/null)
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "停止所有后端相关进程..."
    for PID in $BACKEND_PIDS; do
        echo "  停止进程 (PID: $PID)..."
        kill $PID 2>/dev/null
        sleep 0.5
        if ps -p $PID > /dev/null 2>&1; then
            kill -9 $PID 2>/dev/null
        fi
    done
fi

# 查找并停止所有运行 app.py 的 Python 进程（包括 Flask reloader）
APP_PIDS=$(pgrep -f "python.*app.py" 2>/dev/null)
if [ ! -z "$APP_PIDS" ]; then
    echo "停止所有 app.py 相关进程..."
    for PID in $APP_PIDS; do
        echo "  停止进程 (PID: $PID)..."
        kill $PID 2>/dev/null
        sleep 0.5
        if ps -p $PID > /dev/null 2>&1; then
            kill -9 $PID 2>/dev/null
        fi
    done
fi

# 如果没有找到任何进程，提示
if [ -z "$BACKEND_PIDS" ] && [ -z "$APP_PIDS" ] && [ ! -f "backend.pid" ]; then
    echo "后端服务未运行"
fi

# 停止前端
if [ -f "frontend.pid" ]; then
    FRONTEND_PID=$(cat frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "停止前端服务 (PID: $FRONTEND_PID)..."
        # 先尝试优雅停止
        kill $FRONTEND_PID 2>/dev/null
        sleep 1
        # 如果进程还在，强制停止
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
        rm frontend.pid
    else
        echo "前端服务未运行"
        rm frontend.pid
    fi
fi

# 通过端口查找并停止所有相关进程
FRONTEND_PIDS=$(lsof -ti:8080 2>/dev/null)
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "停止所有前端相关进程..."
    for PID in $FRONTEND_PIDS; do
        echo "  停止进程 (PID: $PID)..."
        kill $PID 2>/dev/null
        sleep 0.5
        if ps -p $PID > /dev/null 2>&1; then
            kill -9 $PID 2>/dev/null
        fi
    done
fi

# 如果没有找到任何进程，提示
if [ -z "$FRONTEND_PIDS" ] && [ ! -f "frontend.pid" ]; then
    echo "前端服务未运行"
fi

echo "服务已停止"

