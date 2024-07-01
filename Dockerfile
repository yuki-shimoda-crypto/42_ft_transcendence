FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MY_USER user
ENV PYTHONPATH /app/PongChat
ENV DJANGO_SETTINGS_MODULE PongChat.settings

# 依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install django psycopg2-binary

# OpenSSL install
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssl && \
    rm -rf /var/lib/apt/lists/*

# entrypoint.sh
COPY tools/docker/web_prod/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# ユーザーを作成して切り替える
RUN useradd -m ${MY_USER}
USER ${MY_USER}

# プロジェクトのコードをコピー
COPY --chown=user:user . .

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Djangoサーバーを起動
CMD ["daphne", "-e", "ssl:8000:privateKey=/app/key.pem:certKey=/app/cert.pem", "PongChat.asgi:application"]
