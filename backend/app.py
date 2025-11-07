from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db
from auth import auth_bp
from auction import auction_bp
from bid import bid_bp
from scheduler import start_scheduler
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_client_ip():
    """获取客户端真实IP地址，考虑代理情况"""
    # 优先检查X-Forwarded-For头（如果有反向代理）
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For可能包含多个IP，取第一个
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return ip
    # 检查X-Real-IP头
    elif request.headers.get('X-Real-Ip'):
        return request.headers.get('X-Real-Ip')
    # 直接连接的IP
    else:
        return request.remote_addr or 'unknown'

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS，允许Authorization头
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 添加请求前钩子来记录请求信息（包括IP）
    @app.before_request
    def log_request_info():
        if request.path.startswith('/api/'):
            client_ip = get_client_ip()
            logger.info(f"[{client_ip}] {request.method} {request.path} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
            
            auth_header = request.headers.get('Authorization', '')
            if auth_header:
                logger.debug(f"[{client_ip}] Authorization header: {auth_header[:50]}...")  # 只打印前50个字符
    
    # 添加请求后钩子来记录响应信息（包括IP和状态码）
    @app.after_request
    def log_response_info(response):
        if request.path.startswith('/api/'):
            client_ip = get_client_ip()
            logger.info(f"[{client_ip}] {request.method} {request.path} - Status: {response.status_code}")
        return response
    
    # JWT错误处理 - 将422错误转换为401
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token已过期，请重新登录', 'type': 'expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        import traceback
        client_ip = get_client_ip()
        logger.warning(f"[{client_ip}] Invalid token error: {error}")
        logger.debug(f"[{client_ip}] Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Token无效，请重新登录', 'type': 'invalid', 'details': str(error)}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': '缺少认证Token，请先登录', 'type': 'missing'}), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token需要刷新，请重新登录', 'type': 'not_fresh'}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token已被撤销，请重新登录', 'type': 'revoked'}), 401
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(auction_bp)
    app.register_blueprint(bid_bp)
    
    # 初始化数据库
    with app.app_context():
        init_db()
    
    # 启动定时任务
    start_scheduler()
    
    @app.route('/')
    def index():
        return {'message': 'Simple Auction API', 'status': 'running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=3000)

