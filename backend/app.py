from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import init_db
from auth import auth_bp
from auction import auction_bp
from bid import bid_bp
from scheduler import start_scheduler

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
    
    # 添加请求前钩子来调试token
    @app.before_request
    def log_request_info():
        if request.path.startswith('/api/'):
            auth_header = request.headers.get('Authorization', '')
            if auth_header:
                print(f"Authorization header: {auth_header[:50]}...")  # 只打印前50个字符
    
    # JWT错误处理 - 将422错误转换为401
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token已过期，请重新登录', 'type': 'expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        import traceback
        print(f"Invalid token error: {error}")
        print(f"Traceback: {traceback.format_exc()}")
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

