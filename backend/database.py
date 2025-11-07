import sqlite3
import os
from config import Config

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建拍卖标的表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            starting_price REAL NOT NULL,
            current_price REAL NOT NULL,
            min_increment REAL DEFAULT 0.01,
            current_bidder_id INTEGER,
            seller_id INTEGER NOT NULL,
            end_time TIMESTAMP NOT NULL,
            status TEXT DEFAULT 'active',
            images TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users(id),
            FOREIGN KEY (current_bidder_id) REFERENCES users(id)
        )
    ''')
    
    # 为现有表添加 min_increment 字段（如果不存在）
    try:
        cursor.execute('ALTER TABLE auctions ADD COLUMN min_increment REAL DEFAULT 0.01')
    except sqlite3.OperationalError:
        # 字段已存在，忽略错误
        pass
    
    # 创建出价记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_id INTEGER NOT NULL,
            bidder_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (auction_id) REFERENCES auctions(id),
            FOREIGN KEY (bidder_id) REFERENCES users(id)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_auctions_status ON auctions(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_auctions_end_time ON auctions(end_time)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bids_auction_id ON bids(auction_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bids_bidder_id ON bids(bidder_id)')
    
    conn.commit()
    conn.close()
    
    # 创建上传目录
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

