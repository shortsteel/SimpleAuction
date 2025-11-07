from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Auction, User
from datetime import datetime
import os
from config import Config

auction_bp = Blueprint('auction', __name__, url_prefix='/api/auctions')

@auction_bp.route('', methods=['POST'])
@jwt_required()
def create_auction():
    """发布拍卖标的"""
    data = request.get_json()
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    starting_price = data.get('starting_price')
    end_time = data.get('end_time')
    images = data.get('images', [])
    min_increment = data.get('min_increment', 0.01)
    
    # 验证输入
    if not title:
        return jsonify({'error': '标的名称不能为空'}), 400
    
    if not description:
        return jsonify({'error': '标的描述不能为空'}), 400
    
    if not starting_price or starting_price <= 0:
        return jsonify({'error': '起拍价必须大于0'}), 400
    
    if not end_time:
        return jsonify({'error': '拍卖结束时间不能为空'}), 400
    
    if not min_increment or min_increment <= 0:
        return jsonify({'error': '最低加价幅度必须大于0'}), 400
    
    # 验证结束时间
    try:
        end_datetime = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        now = datetime.now(end_datetime.tzinfo) if end_datetime.tzinfo else datetime.now()
        
        # 检查是否至少在未来1小时后
        if (end_datetime - now).total_seconds() < 3600:
            return jsonify({'error': '拍卖结束时间必须至少在未来1小时后'}), 400
    except ValueError:
        return jsonify({'error': '结束时间格式不正确'}), 400
    
    seller_id = get_jwt_identity()
    # 将字符串ID转换回整数用于数据库查询
    seller_id = int(seller_id)
    
    # 创建拍卖标的
    auction = Auction.create(title, description, starting_price, end_time, seller_id, images, min_increment)
    
    if not auction:
        return jsonify({'error': '发布失败，请重试'}), 500
    
    return jsonify({
        'message': '发布成功',
        'auction': {
            'id': auction['id'],
            'title': auction['title'],
            'description': auction['description'],
            'starting_price': auction['starting_price'],
            'current_price': auction['current_price'],
            'min_increment': auction.get('min_increment', 0.01),
            'end_time': auction['end_time'],
            'status': auction['status']
        }
    }), 201

@auction_bp.route('', methods=['GET'])
def get_auctions():
    """获取拍卖列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)
    order_by = request.args.get('order_by', 'created_at')
    
    # 验证参数
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20
    
    if status and status not in ['active', 'ended', 'no_bid']:
        status = None
    
    if order_by not in ['created_at', 'end_time']:
        order_by = 'created_at'
    
    auctions, total = Auction.get_list(page, per_page, status, order_by)
    
    # 获取每个拍卖的竞拍者数量
    from models import Bid
    
    # 格式化输出
    result = []
    for auction in auctions:
        # 计算竞拍者数量
        bids = Bid.get_by_auction(auction['id'])
        bidder_count = len(set(bid['bidder_id'] for bid in bids))
        
        # 计算剩余时间
        end_time = datetime.fromisoformat(auction['end_time'].replace('Z', '+00:00'))
        now = datetime.now(end_time.tzinfo) if end_time.tzinfo else datetime.now()
        time_left = (end_time - now).total_seconds()
        
        result.append({
            'id': auction['id'],
            'title': auction['title'],
            'description': auction['description'][:100] + '...' if len(auction['description']) > 100 else auction['description'],
            'starting_price': auction['starting_price'],
            'current_price': auction['current_price'],
            'min_increment': auction.get('min_increment', 0.01),
            'end_time': auction['end_time'],
            'status': auction['status'],
            'images': auction['images'][:1] if auction['images'] else [],  # 只返回第一张图片
            'time_left': max(0, int(time_left)) if auction['status'] == 'active' else 0,
            'seller_username': auction.get('seller_username', ''),
            'bidder_count': bidder_count
        })
    
    return jsonify({
        'auctions': result,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }), 200

@auction_bp.route('/<int:auction_id>', methods=['GET'])
def get_auction_detail(auction_id):
    """获取拍卖详情"""
    auction = Auction.get_by_id(auction_id)
    
    if not auction:
        return jsonify({'error': '拍卖不存在'}), 404
    
    # 获取出价历史
    from models import Bid
    bids = Bid.get_by_auction(auction_id)
    
    # 格式化出价历史（隐藏部分信息）
    bid_history = []
    for bid in bids:
        bid_history.append({
            'amount': bid['amount'],
            'created_at': bid['created_at'],
            'bidder': bid['username'] if len(bid['username']) > 1 else '***'
        })
    
    # 计算剩余时间
    end_time = datetime.fromisoformat(auction['end_time'].replace('Z', '+00:00'))
    now = datetime.now(end_time.tzinfo) if end_time.tzinfo else datetime.now()
    time_left = (end_time - now).total_seconds()
    
    # 获取当前最高出价者信息（部分隐藏）
    current_bidder = None
    if auction['current_bidder_id']:
        bidder = User.get_by_id(auction['current_bidder_id'])
        if bidder:
            current_bidder = {
                'username': bidder['username'] if len(bidder['username']) > 1 else '***'
            }
    
    result = {
        'id': auction['id'],
        'title': auction['title'],
        'description': auction['description'],
        'starting_price': auction['starting_price'],
        'current_price': auction['current_price'],
        'min_increment': auction.get('min_increment', 0.01),
        'current_bidder': current_bidder,
        'end_time': auction['end_time'],
        'status': auction['status'],
        'images': auction['images'],
        'time_left': max(0, int(time_left)) if auction['status'] == 'active' else 0,
        'bid_history': bid_history,
        'seller_id': auction['seller_id'],
        'seller_username': auction.get('seller_username', '')
    }
    
    # 如果是发布者，显示完整信息
    try:
        user_id = get_jwt_identity()
        if user_id is not None:
            # 将字符串ID转换回整数用于比较
            user_id = int(user_id)
            if user_id == auction['seller_id']:
                if auction['current_bidder_id']:
                    bidder = User.get_by_id(auction['current_bidder_id'])
                    if bidder:
                        result['current_bidder'] = {
                            'id': bidder['id'],
                            'username': bidder['username'],
                            'email': bidder['email']
                        }
                # 显示完整出价历史
                result['bid_history'] = [
                    {
                        'amount': bid['amount'],
                        'created_at': bid['created_at'],
                        'bidder': bid['username']
                    }
                    for bid in bids
                ]
    except:
        pass  # 未登录用户
    
    return jsonify(result), 200

@auction_bp.route('/my/listings', methods=['GET'])
@jwt_required()
def get_my_auctions():
    """获取我发布的拍卖"""
    seller_id = get_jwt_identity()
    # 将字符串ID转换回整数用于数据库查询
    seller_id = int(seller_id)
    auctions = Auction.get_by_seller(seller_id)
    
    # 获取每个拍卖的竞拍者数量
    from models import Bid
    result = []
    for auction in auctions:
        bids = Bid.get_by_auction(auction['id'])
        bidder_count = len(set(bid['bidder_id'] for bid in bids))
        
        # 计算剩余时间
        end_time = datetime.fromisoformat(auction['end_time'].replace('Z', '+00:00'))
        now = datetime.now(end_time.tzinfo) if end_time.tzinfo else datetime.now()
        time_left = (end_time - now).total_seconds()
        
        result.append({
            'id': auction['id'],
            'title': auction['title'],
            'description': auction['description'],
            'starting_price': auction['starting_price'],
            'current_price': auction['current_price'],
            'end_time': auction['end_time'],
            'status': auction['status'],
            'images': auction['images'],
            'bidder_count': bidder_count,
            'time_left': max(0, int(time_left)) if auction['status'] == 'active' else 0
        })
    
    return jsonify({'auctions': result}), 200

