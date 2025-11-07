import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    # JWT配置
    JWT_TOKEN_LOCATION = ['headers']  # 从请求头读取token
    JWT_HEADER_NAME = 'Authorization'  # 请求头名称
    JWT_HEADER_TYPE = 'Bearer'  # token类型
    JWT_ALGORITHM = 'HS256'  # 使用HS256算法
    # 支持 Docker 环境的数据库路径
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or os.path.join(os.path.dirname(__file__), 'auction.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

