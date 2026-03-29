"""
Kafka 消费者 - 推荐系统
消费 click / page-view / purchase 三个 Topic
实时统计用户行为，打印推荐结果
"""

from kafka import KafkaConsumer
from .config import Config
import json
from collections import defaultdict
import logging

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

KAFKA_BOOTSTRAP = Config.KAFKA_BOOTSTRAP
TOPICS = Config.KAFKA_CONSUMER_TOPICS
CONSUMER_GROUP_ID = Config.KAFKA_CONSUMER_GROUP_ID

log.info(f"📊 配置的Topics: {TOPICS}")

# ── 统计数据（生产环境写 Redis） ──
click_counts  = defaultdict(int)   # product_id → 点击次数
user_history  = defaultdict(list)  # user_id   → [product_id, ...]
purchase_map  = defaultdict(int)   # product_id → 购买次数


def handle_event(event: dict):
    event_type = event.get('eventType')
    user_id    = event.get('userId')
    product_id = event.get('productId')
    product    = event.get('productName', '未知商品')
    category   = event.get('category', '')

    if event_type == 'click' and product_id:
        click_counts[product_id] += 1
        user_history[user_id].append(product_id)
        log.info(f"👆 点击 | user={user_id} product={product}({product_id}) 累计点击={click_counts[product_id]}")
        print_recommendation(user_id)

    elif event_type == 'page_view':
        log.info(f"👁  浏览 | user={user_id} page={event.get('url','')}")

    elif event_type == 'search':
        keyword = event.get('keyword', '')
        log.info(f"🔍 搜索 | user={user_id} keyword={keyword}")

    elif event_type == 'purchase' and product_id:
        purchase_map[product_id] += 1
        log.info(f"💰 购买 | user={user_id} product={product} price=¥{event.get('price')}")

    elif event_type == 'filter':
        log.info(f"🔍 筛选 | user={user_id} category={category}")


def print_recommendation(user_id: str):
    """简单打印当前推荐（模拟推荐引擎输出）"""
    history = user_history.get(user_id, [])
    if not history:
        return

    # 最近偏好类别
    recent = history[-5:]
    log.info(f"📊 用户 {user_id} 最近浏览: {recent}")

    # 点击量 TOP3
    top3 = sorted(click_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    log.info(f"🔥 全站 TOP3 商品: {top3}")


def main():
    log.info(f"🚀 启动消费者，监听 Topics: {TOPICS}")

    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset='latest',           # 只消费新消息
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
    )

    log.info("✅ 消费者已连接，等待事件...")

    for msg in consumer:
        log.info(f"📨 收到消息 | topic={msg.topic} partition={msg.partition} offset={msg.offset} key={msg.key}")
        try:
            handle_event(msg.value)
        except Exception as e:
            log.error(f"处理消息失败: {e}")


if __name__ == '__main__':
    main()
