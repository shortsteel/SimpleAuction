from apscheduler.schedulers.background import BackgroundScheduler
from models import Auction
from datetime import datetime
import time

def check_and_settle_auctions():
    """检查并结算到期的拍卖"""
    # 获取所有进行中的拍卖
    active_auctions = Auction.get_active_auctions()
    now = datetime.now()
    
    for auction in active_auctions:
        try:
            end_time = datetime.fromisoformat(auction['end_time'].replace('Z', '+00:00'))
            # 如果结束时间已过
            if (end_time - now).total_seconds() <= 0:
                # 检查是否有出价
                from models import Bid
                bids = Bid.get_by_auction(auction['id'])
                
                if len(bids) == 0:
                    # 没有出价，标记为流拍
                    Auction.update_status(auction['id'], 'no_bid')
                else:
                    # 有出价，标记为已结束
                    Auction.update_status(auction['id'], 'ended')
        except Exception as e:
            print(f"Error settling auction {auction['id']}: {e}")
            continue

def start_scheduler():
    """启动定时任务"""
    scheduler = BackgroundScheduler()
    # 每30秒检查一次
    scheduler.add_job(
        func=check_and_settle_auctions,
        trigger="interval",
        seconds=30,
        id='settle_auctions',
        name='结算到期拍卖',
        replace_existing=True
    )
    scheduler.start()
    return scheduler

