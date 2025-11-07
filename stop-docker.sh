#!/bin/bash

# SimpleAuction Docker 容器停止脚本
# 用于停止和清理拍卖系统的 Docker 容器

set -e  # 遇到错误时退出

# 配置变量
IMAGE_NAME="simple-auction"
CONTAINER_NAME="simple-auction-app"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  SimpleAuction Docker 停止脚本${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    exit 1
fi

# 检查容器是否存在
if ! docker ps -a | grep -q ${CONTAINER_NAME}; then
    echo -e "${YELLOW}警告: 容器 '${CONTAINER_NAME}' 不存在${NC}"
    exit 0
fi

# 停止容器
echo -e "${YELLOW}[1/2] 停止容器...${NC}"
if docker ps | grep -q ${CONTAINER_NAME}; then
    docker stop ${CONTAINER_NAME}
    echo -e "${GREEN}✓ 容器已停止${NC}"
else
    echo -e "${YELLOW}容器已经处于停止状态${NC}"
fi
echo ""

# 询问是否删除容器
echo -e "${YELLOW}[2/2] 是否删除容器？${NC}"
echo "选项:"
echo "  1) 仅停止（保留容器，可以快速重启）"
echo "  2) 停止并删除容器（需要重新创建）"
echo "  3) 停止并删除容器和镜像（彻底清理）"
echo ""
read -p "请选择 [1-3] (默认: 1): " choice
choice=${choice:-1}

case $choice in
    1)
        echo ""
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}  停止完成！${NC}"
        echo -e "${GREEN}======================================${NC}"
        echo ""
        echo "容器已停止但未删除，可以使用以下命令重新启动："
        echo -e "  ${GREEN}docker start ${CONTAINER_NAME}${NC}"
        echo ""
        ;;
    2)
        echo ""
        echo "删除容器..."
        docker rm ${CONTAINER_NAME}
        echo -e "${GREEN}✓ 容器已删除${NC}"
        echo ""
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}  停止并删除完成！${NC}"
        echo -e "${GREEN}======================================${NC}"
        echo ""
        echo "容器已删除，重新启动需要运行："
        echo -e "  ${GREEN}./start-docker.sh${NC}"
        echo ""
        ;;
    3)
        echo ""
        echo "删除容器..."
        docker rm ${CONTAINER_NAME}
        echo -e "${GREEN}✓ 容器已删除${NC}"
        
        echo "删除镜像..."
        if docker images | grep -q ${IMAGE_NAME}; then
            docker rmi ${IMAGE_NAME}
            echo -e "${GREEN}✓ 镜像已删除${NC}"
        else
            echo -e "${YELLOW}镜像不存在，跳过${NC}"
        fi
        
        echo ""
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}  彻底清理完成！${NC}"
        echo -e "${GREEN}======================================${NC}"
        echo ""
        echo "容器和镜像已删除，重新启动需要运行："
        echo -e "  ${GREEN}./start-docker.sh${NC}"
        echo ""
        ;;
    *)
        echo -e "${RED}无效的选择${NC}"
        exit 1
        ;;
esac

# 显示当前运行的容器
running_containers=$(docker ps --filter "name=${IMAGE_NAME}" --format "{{.Names}}" | wc -l)
if [ $running_containers -eq 0 ]; then
    echo -e "${YELLOW}当前没有运行的 ${IMAGE_NAME} 相关容器${NC}"
else
    echo -e "${GREEN}当前运行的容器:${NC}"
    docker ps --filter "name=${IMAGE_NAME}"
fi

