#!/bin/sh
set -e

# 使用环境变量替换nginx配置文件中的占位符
envsubst '$SERVER_NAME $BACKEND_HOST $BACKEND_PORT' < /etc/nginx/conf.d/activityTracker.conf.template > /etc/nginx/conf.d/activityTracker.conf

# 启动nginx
exec nginx -g 'daemon off;'
