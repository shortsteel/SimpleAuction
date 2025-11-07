from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Auction, Bid, User
from datetime import datetime

bid_bp = Blueprint('bid', __name__, url_prefix='/api/auctions')

@bid_bp.route('/<int:auction_id>/bids', methods=['POST'])
@jwt_required()
def create_bid(auction_id):
    """参与竞拍（出价）"""
    data = request.get_json()
    amount = data.get('amount')
    
    if not amount or amount <= 0:
        return jsonify({'error': '出价金额必须大于0'}), 400
    
    bidder_id = get_jwt_identity()
    # 将字符串ID转换回整数用于数据库查询和比较
    bidder_id = int(bidder_id)
    
    # 获取拍卖信息
    auction = Auction.get_by_id(auction_id)
    if not auction:
        return jsonify({'error': '拍卖不存在'}), 404
    
    # 检查是否是自己的拍卖
    if auction['seller_id'] == bidder_id:
        return jsonify({'error': '不能对自己的拍卖出价'}), 400
    
    # 检查拍卖状态
    if auction['status'] != 'active':
        return jsonify({'error': '拍卖已结束或已流拍'}), 400
    
    # 检查是否已到结束时间
    end_time = datetime.fromisoformat(auction['end_time'].replace('Z', '+00:00'))
    now = datetime.now(end_time.tzinfo) if end_time.tzinfo else datetime.now()
    if (end_time - now).total_seconds() <= 0:
        return jsonify({'error': '拍卖已结束'}), 400
    
    # 验证出价金额
    current_price = auction['current_price']
    min_increment = auction.get('min_increment', 0.01)
    min_bid_amount = current_price + min_increment
    
    if amount < min_bid_amount:
        return jsonify({'error': f'出价金额必须至少为当前最高价加上最低加价幅度，即 {min_bid_amount:.2f}'}), 400
    
    # 创建出价记录
    bid = Bid.create(auction_id, bidder_id, amount)
    if not bid:
        return jsonify({'error': '出价失败，请重试'}), 500
    
    # 更新拍卖当前最高价
    Auction.update_current_price(auction_id, amount, bidder_id)
    
    return jsonify({
        'message': '出价成功',
        'bid': {
            'id': bid['id'],
            'amount': bid['amount'],
            'created_at': bid['created_at']
        }
    }), 201

@bid_bp.route('/my/bids', methods=['GET'])
@jwt_required()
def get_my_bids():
    """获取我的竞拍记录"""
    bidder_id = get_jwt_identity()
    # 将字符串ID转换回整数用于数据库查询
    bidder_id = int(bidder_id)
    bids = Bid.get_by_bidder(bidder_id)
    
    # 格式化输出
    result = []
    for bid in bids:
        # 计算剩余时间
        end_time = datetime.fromisoformat(bid['end_time'].replace('Z', '+00:00'))
        now = datetime.now(end_time.tzinfo) if end_time.tzinfo else datetime.now()
        time_left = (end_time - now).total_seconds()
        
        # 判断状态
        original_status = bid['status']
        status = original_status
        
        # 如果拍卖状态是 active 但时间已过，需要检查实际状态
        if status == 'active' and time_left <= 0:
            # 时间已过，检查是否有出价（通过检查 current_bidder_id 或 bids 数量）
            # 如果有出价，应该是 ended；如果没有出价，应该是 no_bid
            # 检查是否有出价记录
            bids_count = len(Bid.get_by_auction(bid['auction_id']))
            if bids_count == 0:
                status = 'no_bid'
            else:
                status = 'ended'
        
        # 判断用户是否是最终中标者（当拍卖结束时）
        # 只有最高出价的那个记录才标记为中标
        is_winner = False
        if status == 'ended' and bid.get('current_bidder_id') == bidder_id:
            # 拍卖已结束，且当前用户是最高出价者
            # 只有出价金额等于当前最高价的记录才是中标记录
            if bid['amount'] == bid['current_price']:
                is_winner = True
        
        result.append({
            'id': bid['id'],
            'auction_id': bid['auction_id'],
            'title': bid['title'],
            'amount': bid['amount'],
            'current_price': bid['current_price'],
            'is_highest': bid.get('is_highest', False) and original_status == 'active' and time_left > 0,
            'is_winner': is_winner,  # 是否中标
            'status': status,
            'end_time': bid['end_time'],
            'time_left': max(0, int(time_left)) if original_status == 'active' and time_left > 0 else 0,
            'created_at': bid['created_at']
        })
    
    return jsonify({'bids': result}), 200

