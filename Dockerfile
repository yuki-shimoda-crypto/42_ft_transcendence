FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MY_USER user

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install django

# ユーザーを作成して切り替える
RUN useradd -m ${MY_USER}
USER ${MY_USER}

# プロジェクトのコードをコピー
COPY --chown=user:user . .

# Djangoサーバーを起動
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
