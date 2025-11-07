#!/bin/bash

# SimpleAuction Docker 快速重启脚本
# 停止旧容器并重新启动

set -e

# 配置变量
IMAGE_NAME="simple-auction"
CONTAINER_NAME="simple-auction-app"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  SimpleAuction 快速重启${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# 停止并删除旧容器
echo -e "${YELLOW}[1/2] 清理旧容器...${NC}"
if docker ps -a | grep -q ${CONTAINER_NAME}; then
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    echo -e "${GREEN}✓ 旧容器已清理${NC}"
fi
echo ""

# 重新启动
echo -e "${YELLOW}[2/2] 重新启动容器...${NC}"
echo "运行启动脚本..."
./start-docker.sh

