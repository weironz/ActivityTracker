"""
配置管理模块
使用环境变量和.env文件管理配置
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# 尝试从项目根目录加载.env文件
# 支持不同运行环境：Docker容器、本地开发等
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)
    print(f"[OK] Loaded config file: {env_path}")
else:
    load_dotenv()  # 尝试加载当前目录的.env文件
    print("[WARNING] No root .env file found, using environment variables or defaults")

class Config:
    """基础配置类"""

    # Kafka配置
    KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092')

    # Kafka Topics
    KAFKA_TOPICS = {
        'page_view': os.getenv('KAFKA_TOPIC_PAGE_VIEW', 'page-view'),
        'search': os.getenv('KAFKA_TOPIC_SEARCH', 'search'),
        'click': os.getenv('KAFKA_TOPIC_CLICK', 'click'),
        'purchase': os.getenv('KAFKA_TOPIC_PURCHASE', 'purchase'),
        'filter': os.getenv('KAFKA_TOPIC_FILTER', 'user-action'),
    }

    # Kafka消费者配置
    KAFKA_CONSUMER_TOPICS = [
        'click',
        'page-view',
        'purchase'
    ]

    KAFKA_CONSUMER_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP_ID', 'recommendation-engine')

    # Flask配置
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # 推荐系统配置
    RECOMMENDATION_TOP_N = int(os.getenv('RECOMMENDATION_TOP_N', 4))
    RECOMMENDATION_HISTORY_SIZE = int(os.getenv('RECOMMENDATION_HISTORY_SIZE', 5))
