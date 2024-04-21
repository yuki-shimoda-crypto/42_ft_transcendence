#!/bin/bash
set -e

# gpg-agent を起動
gpg-agent --daemon

# 環境変数からデータベース接続情報を取得
DB_HOST=db
DB_USER=${POSTGRES_USER}
DB_NAME=${POSTGRES_DB}
DB_PORT=${POSTGRES_PORT}
DB_PASSWORD=${POSTGRES_PASSWORD}

# .pg_service.conf ファイルを生成
cat << EOF > ~/.pg_service.conf
[pong_chat]
host=$DB_HOST
user=$DB_USER
dbname=$DB_NAME
port=$DB_PORT
EOF

# .pgpass ファイルを生成
echo "$DB_HOST:$DB_PORT:$DB_NAME:$DB_USER:$DB_PASSWORD" > PongChat/.pgpass
chmod 0600 PongChat/.pgpass

# Dockerコンテナで指定されたコマンドを実行（通常はDjangoアプリケーションの起動など）
exec "$@"