#!/bin/bash
set -e

# Dockerコンテナで指定されたコマンドを実行（通常はDjangoアプリケーションの起動など）
exec "$@"
