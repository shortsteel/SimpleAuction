from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import json
import sqlite3
from datetime import datetime

class User:
    @staticmethod
    def create(username, email, password):
        """创建新用户"""
        conn = get_db()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            conn.commit()
            user_id = cursor.lastrowid
            return User.get_by_id(user_id)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(user_id):
        """根据ID获取用户"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_username(username):
        """根据用户名获取用户"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_email(email):
        """根据邮箱获取用户"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def verify_password(user, password):
        """验证密码"""
        return check_password_hash(user['password'], password)

class Auction:
    @staticmethod
    def create(title, description, starting_price, end_time, seller_id, images=None):
        """创建拍卖标的"""
        conn = get_db()
        cursor = conn.cursor()
        images_json = json.dumps(images) if images else '[]'
        try:
            cursor.execute('''
                INSERT INTO auctions (title, description, starting_price, current_price, 
                                   seller_id, end_time, images)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, starting_price, starting_price, seller_id, end_time, images_json))
            conn.commit()
            auction_id = cursor.lastrowid
            return Auction.get_by_id(auction_id)
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(auction_id):
        """根据ID获取拍卖标的"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auctions WHERE id = ?', (auction_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            auction = dict(row)
            auction['images'] = json.loads(auction['images']) if auction['images'] else []
            return auction
        return None
    
    @staticmethod
    def get_list(page=1, per_page=20, status=None, order_by='created_at'):
        """获取拍卖列表"""
        conn = get_db()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM auctions WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        if order_by == 'created_at':
            query += ' ORDER BY created_at DESC'
        elif order_by == 'end_time':
            query += ' ORDER BY end_time ASC'
        
        query += ' LIMIT ? OFFSET ?'
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        auctions = []
        for row in rows:
            auction = dict(row)
            auction['images'] = json.loads(auction['images']) if auction['images'] else []
            auctions.append(auction)
        
        # 获取总数
        count_query = 'SELECT COUNT(*) as total FROM auctions WHERE 1=1'
        count_params = []
        if status:
            count_query += ' AND status = ?'
            count_params.append(status)
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']
        
        conn.close()
        return auctions, total
    
    @staticmethod
    def get_by_seller(seller_id):
        """获取用户发布的拍卖"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auctions WHERE seller_id = ? ORDER BY created_at DESC', (seller_id,))
        rows = cursor.fetchall()
        auctions = []
        for row in rows:
            auction = dict(row)
            auction['images'] = json.loads(auction['images']) if auction['images'] else []
            auctions.append(auction)
        conn.close()
        return auctions
    
    @staticmethod
    def update_current_price(auction_id, new_price, bidder_id):
        """更新当前最高价"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE auctions 
            SET current_price = ?, current_bidder_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_price, bidder_id, auction_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_status(auction_id, status):
        """更新拍卖状态"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE auctions 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, auction_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_active_auctions():
        """获取所有进行中的拍卖"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auctions WHERE status = ?', ('active',))
        rows = cursor.fetchall()
        auctions = []
        for row in rows:
            auction = dict(row)
            auction['images'] = json.loads(auction['images']) if auction['images'] else []
            auctions.append(auction)
        conn.close()
        return auctions

class Bid:
    @staticmethod
    def create(auction_id, bidder_id, amount):
        """创建出价记录"""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO bids (auction_id, bidder_id, amount)
                VALUES (?, ?, ?)
            ''', (auction_id, bidder_id, amount))
            conn.commit()
            bid_id = cursor.lastrowid
            return Bid.get_by_id(bid_id)
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(bid_id):
        """根据ID获取出价记录"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bids WHERE id = ?', (bid_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_auction(auction_id):
        """获取拍卖的所有出价记录"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, u.username 
            FROM bids b
            JOIN users u ON b.bidder_id = u.id
            WHERE b.auction_id = ?
            ORDER BY b.created_at DESC
        ''', (auction_id,))
        rows = cursor.fetchall()
        bids = [dict(row) for row in rows]
        conn.close()
        return bids
    
    @staticmethod
    def get_by_bidder(bidder_id):
        """获取用户的所有出价记录"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, a.title, a.status, a.end_time, a.current_price, a.current_bidder_id
            FROM bids b
            JOIN auctions a ON b.auction_id = a.id
            WHERE b.bidder_id = ?
            ORDER BY b.created_at DESC
        ''', (bidder_id,))
        rows = cursor.fetchall()
        bids = []
        for row in rows:
            bid = dict(row)
            # 判断是否是最高出价者
            bid['is_highest'] = (bid['amount'] == bid['current_price'] and 
                               bid['current_bidder_id'] == bidder_id)
            bids.append(bid)
        conn.close()
        return bids

