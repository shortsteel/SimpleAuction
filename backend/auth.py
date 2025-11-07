from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
import re
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # 验证输入
    if not username:
        return jsonify({'error': '用户名不能为空'}), 400
    
    if not email:
        return jsonify({'error': '邮箱不能为空'}), 400
    
    # 验证邮箱格式
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'error': '邮箱格式不正确'}), 400
    
    # 验证密码
    if len(password) < 8:
        return jsonify({'error': '密码至少需要8位'}), 400
    
    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        return jsonify({'error': '密码必须包含字母和数字'}), 400
    
    # 检查用户名是否已存在
    if User.get_by_username(username):
        return jsonify({'error': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if User.get_by_email(email):
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # 创建用户
    user = User.create(username, email, password)
    if not user:
        return jsonify({'error': '注册失败，请重试'}), 500
    
    # 生成token (JWT要求subject必须是字符串)
    access_token = create_access_token(identity=str(user['id']))
    
    return jsonify({
        'message': '注册成功',
        'token': access_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    username_or_email = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username_or_email or not password:
        return jsonify({'error': '用户名/邮箱和密码不能为空'}), 400
    
    # 查找用户（通过用户名或邮箱）
    user = User.get_by_username(username_or_email)
    if not user:
        user = User.get_by_email(username_or_email)
    
    if not user:
        return jsonify({'error': '用户名/邮箱或密码错误'}), 401
    
    # 验证密码
    if not User.verify_password(user, password):
        return jsonify({'error': '用户名/邮箱或密码错误'}), 401
    
    # 生成token (JWT要求subject必须是字符串)
    access_token = create_access_token(identity=str(user['id']))
    
    return jsonify({
        'message': '登录成功',
        'token': access_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    # JWT是无状态的，客户端删除token即可
    return jsonify({'message': '登出成功'}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    # 将字符串ID转换回整数用于数据库查询
    user = User.get_by_id(int(user_id))
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email']
    }), 200

