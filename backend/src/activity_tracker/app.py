"""
Kafka 活动追踪系统 - 后端服务
功能：
  - POST /track        接收前端埋点事件，写入 Kafka
  - GET  /recommendations  从推荐引擎获取推荐
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from .config import Config
import json
import logging

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

KAFKA_BOOTSTRAP = Config.KAFKA_BOOTSTRAP
TOPICS = Config.KAFKA_TOPICS

# ── Kafka Producer ──
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all',           # 等待所有副本确认（单节点下等同于 acks=1）
        retries=3,
    )
    log.info("✅ Kafka Producer 连接成功")
except NoBrokersAvailable:
    producer = None
    log.warning("⚠️  Kafka 未运行，事件将仅打印到日志（演示模式）")


def send_to_kafka(topic: str, key: str, value: dict) -> dict:
    """发送消息到 Kafka，返回 offset 等元信息"""
    if producer is None:
        log.info(f"[DEMO] Topic={topic} Key={key} Value={value}")
        return {"offset": None, "partition": 0, "topic": topic}

    future = producer.send(topic, key=key, value=value)
    metadata = future.get(timeout=5)
    log.info(f"✅ 写入 Kafka | topic={metadata.topic} partition={metadata.partition} offset={metadata.offset}")
    return {
        "topic":     metadata.topic,
        "partition": metadata.partition,
        "offset":    metadata.offset,
    }


# ── 推荐引擎（简单版：基于热度统计） ──
# 生产环境可替换为 Redis + 实时 Consumer 写入的统计数据
from collections import defaultdict
click_counts = defaultdict(int)   # { product_id: count }

PRODUCTS = [
    {"id": 1,  "name": "AirPods Pro 2",  "category": "数码", "price": 1799, "emoji": "🎧"},
    {"id": 2,  "name": "机械键盘 87键",   "category": "数码", "price": 459,  "emoji": "⌨️"},
    {"id": 3,  "name": "4K 显示器 27寸",  "category": "数码", "price": 2299, "emoji": "🖥️"},
    {"id": 4,  "name": "无线充电底座",    "category": "数码", "price": 199,  "emoji": "🔋"},
    {"id": 5,  "name": "北欧风台灯",      "category": "家居", "price": 329,  "emoji": "💡"},
    {"id": 6,  "name": "香氛蜡烛套装",    "category": "家居", "price": 189,  "emoji": "🕯️"},
    {"id": 7,  "name": "懒人沙发豆袋",    "category": "家居", "price": 599,  "emoji": "🛋️"},
    {"id": 8,  "name": "复古牛仔夹克",    "category": "服饰", "price": 699,  "emoji": "🧥"},
    {"id": 9,  "name": "手工真皮钱包",    "category": "服饰", "price": 399,  "emoji": "👛"},
    {"id": 10, "name": "联名帆布鞋",      "category": "服饰", "price": 529,  "emoji": "👟"},
    {"id": 11, "name": "日本抹茶礼盒",    "category": "食品", "price": 128,  "emoji": "🍵"},
    {"id": 12, "name": "手工巧克力礼盒",  "category": "食品", "price": 228,  "emoji": "🍫"},
]

# 用户点击历史 { user_id: [product_id, ...] }
user_history = defaultdict(list)


def get_recommendations(user_id: str, top_n: int = 4) -> list:
    """
    简单推荐逻辑：
    1. 找出用户最近点击的商品类别
    2. 推荐同类别中点击量最高的商品（排除已看过的）
    """
    history = user_history.get(user_id, [])

    if not history:
        # 无历史：推荐全站最热
        sorted_products = sorted(PRODUCTS, key=lambda p: click_counts[p['id']], reverse=True)
        return sorted_products[:top_n]

    # 找最近偏好的类别
    recent_ids = history[-5:]   # 取最近 5 个
    recent_cats = [p['category'] for p in PRODUCTS if p['id'] in recent_ids]
    preferred_cat = max(set(recent_cats), key=recent_cats.count) if recent_cats else None

    # 同类 + 排除历史
    candidates = [
        p for p in PRODUCTS
        if p['id'] not in history and (preferred_cat is None or p['category'] == preferred_cat)
    ]

    # 按点击量排序
    candidates.sort(key=lambda p: click_counts[p['id']], reverse=True)

    # 不够则补充其他类别
    if len(candidates) < top_n:
        others = [p for p in PRODUCTS if p['id'] not in history and p not in candidates]
        others.sort(key=lambda p: click_counts[p['id']], reverse=True)
        candidates += others

    return candidates[:top_n]


# ── API 路由 ──

@app.post('/track')
def track():
    """接收前端埋点事件，写入对应 Kafka Topic"""
    event = request.json
    if not event:
        return jsonify({"error": "empty body"}), 400

    event_type = event.get('eventType', 'unknown')
    user_id    = event.get('userId', 'anonymous')
    product_id = event.get('productId')

    # 路由到对应 Topic
    topic = TOPICS.get(event_type, 'user-action')

    # 更新内存统计（生产环境由 Consumer 负责）
    if event_type == 'click' and product_id:
        click_counts[product_id] += 1
        user_history[user_id].append(product_id)

    result = send_to_kafka(topic, key=user_id, value=event)
    return jsonify({"status": "ok", **result})


@app.get('/recommendations')
def recommendations():
    """返回个性化推荐商品列表"""
    user_id = request.args.get('userId', 'anonymous')
    recs = get_recommendations(user_id)
    return jsonify({"userId": user_id, "recommendations": recs})


@app.get('/health')
def health():
    return jsonify({"status": "ok", "kafka": producer is not None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
