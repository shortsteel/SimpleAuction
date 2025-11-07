#!/bin/bash

# SimpleAuction Docker 容器启动脚本
# 用于构建和启动拍卖系统的 Docker 容器

set -e  # 遇到错误时退出

# 配置变量
IMAGE_NAME="simple-auction"
CONTAINER_NAME="simple-auction-app"
HOST_PORT=18080
CONTAINER_PORT=80

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  SimpleAuction Docker 启动脚本${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装，请先安装 Docker${NC}"
    exit 1
fi

# 检查 Docker 服务是否运行
if ! docker info &> /dev/null; then
    echo -e "${RED}错误: Docker 服务未运行，请先启动 Docker${NC}"
    exit 1
fi

# 创建数据目录（如果不存在）
echo -e "${YELLOW}[1/5] 创建数据目录...${NC}"
mkdir -p data/database
mkdir -p data/uploads
mkdir -p data/logs
echo -e "${GREEN}✓ 数据目录已准备${NC}"
echo ""

# 停止并删除旧容器（如果存在）
echo -e "${YELLOW}[2/5] 检查并清理旧容器...${NC}"
if docker ps -a | grep -q ${CONTAINER_NAME}; then
    echo "停止旧容器..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    echo "删除旧容器..."
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    echo -e "${GREEN}✓ 旧容器已清理${NC}"
else
    echo -e "${GREEN}✓ 没有发现旧容器${NC}"
fi
echo ""

# 构建 Docker 镜像
echo -e "${YELLOW}[3/5] 构建 Docker 镜像...${NC}"
echo "这可能需要几分钟时间，请耐心等待..."
docker build -t ${IMAGE_NAME} .
echo -e "${GREEN}✓ 镜像构建完成${NC}"
echo ""

# 启动容器
echo -e "${YELLOW}[4/5] 启动 Docker 容器...${NC}"
docker run -d \
  --name ${CONTAINER_NAME} \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  -e DATABASE_PATH=/app/data/database/auction.db \
  -v "$(pwd)/data/database:/app/data/database" \
  -v "$(pwd)/data/uploads:/app/backend/uploads" \
  -v "$(pwd)/data/logs:/app/logs" \
  --restart unless-stopped \
  ${IMAGE_NAME}

echo -e "${GREEN}✓ 容器已启动${NC}"
echo ""

# 等待服务启动
echo -e "${YELLOW}[5/5] 等待服务启动...${NC}"
sleep 3

# 检查容器状态
if docker ps | grep -q ${CONTAINER_NAME}; then
    echo -e "${GREEN}✓ 容器运行正常${NC}"
    echo ""
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}  启动成功！${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo ""
    echo -e "访问地址: ${GREEN}http://localhost:${HOST_PORT}${NC}"
    echo ""
    echo "常用命令:"
    echo "  查看容器日志: docker logs -f ${CONTAINER_NAME}"
    echo "  停止容器:     docker stop ${CONTAINER_NAME}"
    echo "  启动容器:     docker start ${CONTAINER_NAME}"
    echo "  重启容器:     docker restart ${CONTAINER_NAME}"
    echo "  删除容器:     docker rm -f ${CONTAINER_NAME}"
    echo ""
else
    echo -e "${RED}✗ 容器启动失败${NC}"
    echo "查看错误日志:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi

