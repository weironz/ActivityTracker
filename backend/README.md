# Activity Tracker Backend

Kafka 活动追踪系统 - 后端服务

## 功能

- **POST /track** - 接收前端埋点事件，写入 Kafka
- **GET /recommendations** - 从推荐引擎获取推荐
- **Consumer** - 消费 Kafka 消息，实时统计用户行为

## 本地开发

### 安装依赖

```bash
uv sync
```

### 启动应用

```bash
uv run activity-tracker app
```

或者直接运行：

```bash
uv run python -m activity_tracker.app
```

### 启动消费者

```bash
uv run activity-tracker consumer
```

或者直接运行：

```bash
uv run python -m activity_tracker.consumer
```

## Docker 构建

```bash
docker build -t activity-tracker-backend .
```

## 环境变量

- `KAFKA_BOOTSTRAP` - Kafka 服务器地址 (默认: localhost:9092)
- `FLASK_HOST` - Flask 服务器地址 (默认: 0.0.0.0)
- `FLASK_PORT` - Flask 端口 (默认: 5000)
- `FLASK_DEBUG` - Flask 调试模式 (默认: True)
- `LOG_LEVEL` - 日志级别 (默认: INFO)
