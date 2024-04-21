FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MY_USER user

# 依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install django psycopg2-binary

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
CMD ["python", "PongChat/manage.py", "runserver", "0.0.0.0:8000"]
