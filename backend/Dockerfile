FROM python:3.12-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制 pyproject.toml 和 uv.lock
COPY pyproject.toml uv.lock ./

# 使用 uv 同步依赖
RUN uv sync --frozen --no-cache

# 复制应用代码（.dockerignore会排除.env文件等敏感信息）
COPY . .

# 确保使用 uv 安装的 Python
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

# 启动命令（可被 docker-compose override）
CMD ["uv", "run", "python", "-m", "activity_tracker.app"]
