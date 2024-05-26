#!/bin/bash
set -e

# gpg-agent を起動
gpg-agent --daemon

# Dockerコンテナで指定されたコマンドを実行（通常はDjangoアプリケーションの起動など）
exec "$@"
