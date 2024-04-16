#!/bin/bash
# docker-entrypoint.sh

# gpg-agent を起動
gpg-agent --daemon

# 引数で指定されたコマンドを実行
exec "$@"
