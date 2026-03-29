FROM nginx:1.29.7-alpine

# 复制前端文件到 nginx 的静态文件目录
COPY index.html /usr/share/nginx/html/index.html

# 复制样式和脚本文件
COPY styles/ /usr/share/nginx/html/styles/
COPY scripts/ /usr/share/nginx/html/scripts/

# 复制 nginx 配置文件模板
COPY activityTracker.conf.template /etc/nginx/conf.d/activityTracker.conf.template

# 复制启动脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh

# 设置启动脚本执行权限
RUN chmod +x /docker-entrypoint.sh

# 设置默认环境变量
ENV SERVER_NAME=localhost
ENV BACKEND_HOST=backend
ENV BACKEND_PORT=5000

# 暴露端口
EXPOSE 80

# 使用启动脚本
ENTRYPOINT ["/docker-entrypoint.sh"]