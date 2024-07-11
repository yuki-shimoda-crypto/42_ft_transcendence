#!/bin/bash
set -e

if [ ! -f /app/key.pem ] || [ ! -f /app/cert.pem ]; then
    openssl req -x509 -newkey rsa:4096 -keyout /app/key.pem -out /app/cert.pem -days 365 -nodes -subj "/CN=localhost"
    chown ${MY_USER}:${MY_USER} /app/key.pem /app/cert.pem
fi

PongChat/manage.py migrate
PongChat/manage.py compilemessages

# Dockerコンテナで指定されたコマンドを実行（通常はDjangoアプリケーションの起動など）
exec "$@"
