# 多阶段构建：前端构建阶段
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 使用国内 npm 镜像源加速
RUN npm config set registry https://registry.npmmirror.com

# 安装前端依赖
RUN npm install

# 复制前端源代码
COPY frontend/ ./

# 构建前端
RUN npm run build

# 后端运行阶段
FROM python:3.11-slim

WORKDIR /app

# 使用阿里云镜像源加速 apt-get
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖（包括 nginx）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt ./

# 使用阿里云 PyPI 镜像源加速并安装 Python 依赖
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip && \
    pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 复制后端代码
COPY backend/ ./backend/

# 从前端构建阶段复制构建好的前端文件
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# 配置 nginx
RUN printf 'server {\n\
    listen 80;\n\
    server_name _;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    \n\
    # 前端路由\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
    \n\
    # API 代理到后端\n\
    location /api {\n\
        proxy_pass http://127.0.0.1:3000;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
        proxy_set_header X-Forwarded-Proto $scheme;\n\
    }\n\
    \n\
    # 上传文件代理\n\
    location /uploads {\n\
        proxy_pass http://127.0.0.1:3000;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
    }\n\
}\n' > /etc/nginx/sites-available/default

# 配置 supervisor 来管理 nginx 和 Flask
RUN printf '[supervisord]\n\
nodaemon=true\n\
\n\
[program:nginx]\n\
command=/usr/sbin/nginx -g "daemon off;"\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/nginx/error.log\n\
stdout_logfile=/var/log/nginx/access.log\n\
\n\
[program:flask]\n\
command=python -c "from app import create_app; app = create_app(); app.run(host='\''0.0.0.0'\'', port=3000, debug=False)"\n\
directory=/app/backend\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/app/logs/backend.log\n\
stdout_logfile=/app/logs/backend.log\n\
environment=PYTHONUNBUFFERED=1\n' > /etc/supervisor/conf.d/supervisord.conf

# 创建必要的目录
RUN mkdir -p /app/logs && \
    mkdir -p /app/data/database && \
    mkdir -p /app/backend/uploads

# 暴露端口
EXPOSE 80

# 启动 supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

