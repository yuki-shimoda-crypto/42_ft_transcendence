# Djangoアプリケーションのモニタリングセットアップ

[English version](./MONITOR_README.md)

このドキュメントでは、ft_transcendenceプロジェクトのDjangoアプリケーションのモニタリングセットアップ方法について説明します。

## 目次

1. [django-prometheusのセットアップ](#django-prometheusのセットアップ)
2. [PrometheusとGrafanaのDocker Composeによるセットアップ](#prometheusとgrafanaのdocker-composeによるセットアップ)
3. [Grafanaダッシュボードの追加](#grafanaダッシュボードの追加)

## django-prometheusのセットアップ

[django-prometheus](https://github.com/korfuri/django-prometheus)は、Djangoアプリケーションの監視メトリクスをPrometheusにエクスポートするためのPythonライブラリです。

### インストール

```bash
pip install django-prometheus
```

### 設定

1. `settings.py`に以下を追加:

```python
INSTALLED_APPS = [
   ...
   "django_prometheus",
]

MIDDLEWARE = (
    ["django_prometheus.middleware.PrometheusBeforeMiddleware"]
    + MIDDLEWARE
    + ["django_prometheus.middleware.PrometheusAfterMiddleware"]
)
```

2. `urls.py`に以下を追加:

```python
urlpatterns = [
    ...
    path("prometheus/", include("django_prometheus.urls")),
]
```

これにより、`/prometheus/metrics`エンドポイントでメトリクスにアクセスできるようになります。

## PrometheusとGrafanaのDocker Composeによるセットアップ

### Docker Compose設定

`docker-compose.monitoring.yml`ファイルを作成し、以下の内容を追加:

```yaml
version: "3.8"

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data: {}
  grafana-data: {}

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
      - "--web.enable-lifecycle"
    ports:
      - 9090:9090
    networks:
      - monitoring

  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - monitoring
```

### Prometheus設定

`prometheus.yml`ファイルを作成し、以下の内容を追加:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: "django_app"
    metrics_path: "/prometheus/metrics"
    static_configs:
      - targets: ["host.docker.internal:8080"]
```

注意: `targets`の値は、Djangoアプリケーションの実際のホストとポートに合わせて調整してください。

### Docker Compose起動

```bash
docker-compose -f docker-compose.monitoring.yml up --build
```

これにより、以下のサービスが利用可能になります:

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

## Grafanaダッシュボードの追加

### データソースの追加

1. Grafanaにログイン（デフォルトの認証情報: admin/admin）
2. 左側のメニューから「Configuration」→「Data sources」を選択
3. 「Add data source」をクリック
4. Prometheusを選択
5. 以下の設定を行う:
   - Name: Prometheus
   - URL: `http://prometheus:9090`
6. 「Save & Test」をクリック

### ダッシュボードのインポート

1. 左側のメニューから「Create」→「Import」を選択
2. 「Import via grafana.com」に[Django Prometheus](https://grafana.com/grafana/dashboards/17658-django/)ダッシュボードのURLを入力
3. 「Load」をクリック
4. データソースとしてPrometheusを選択
5. 「Import」をクリック

これで、Djangoアプリケーションのメトリクスを表示するダッシュボードが利用可能になります。

## トラブルシューティング

- メトリクスが表示されない場合は、Djangoアプリケーションが正しく実行されていること、およびPrometheusの設定が正しいことを確認してください。
- Grafanaでデータソースの接続に失敗する場合は、ネットワーク設定を確認し、PrometheusコンテナがGrafanaコンテナから到達可能であることを確認してください。

## 参考リンク

- [django-prometheus GitHub](https://github.com/korfuri/django-prometheus)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
