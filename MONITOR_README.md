# Djangoアプリケーションのモニタリングセットアップ

## django-prometheusのセットアップ

[django-prometheus](https://github.com/korfuri/django-prometheus)というPythonライブラリを使用して、Djangoの監視メトリクスをPrometheusにエクスポートすることができます。以下のコマンドを実行して簡単にインストールできます。

```bash
pip install django-prometheus
```

次に、`settings.py`ファイルに以下の設定を追加します。

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

また、`urls.py`ファイルに以下の設定を追加して、django-prometheusがエクスポートするメトリクスにアクセスできるようにします。

```python
urlpatterns = [
    ...
    path("prometheus/", include("django_prometheus.urls")),
]
```

これで、`/prometheus/metrics`エンドポイントにアクセスすることでメトリクスにアクセスできるようになります。

## PrometheusとGrafanaのDocker Composeによるセットアップ

以下は、PrometheusとGrafanaをセットアップするためのDocker Composeファイルです。`docker-compose.monitoring.yml`という名前で保存してください。

```yml
version: '3.8'

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
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - 9090:9090
    networks:
      - monitoring

  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    ports:
      - '3000:3000'
    volumes:
      - grafana-data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - monitoring
```

また、Prometheusの設定ファイルである`prometheus.yml`を作成し、以下のように設定します。

```yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'django_app'
    metrics_path: '/prometheus/metrics'
    static_configs:
      - targets: ['host.docker.internal:8080']
```

上記の設定では、Prometheusがホストマシンの`localhost:8080/prometheus/metrics`からメトリクスを取得します。

以上の設定を行った後、以下のコマンドを実行してDocker Composeを起動し、イメージをビルドします。

```bash
docker-compose -f docker-compose.monitoring.yml up --build
```

これで、Grafanaには`localhost:3000`、Prometheusには`localhost:9090`でアクセスできるようになります。



## Grafanaダッシュボードの追加

このセクションでは、アプリケーションのメトリクスを監視するためのダッシュボードを追加する方法を探ります。Grafanaがコミュニティ主導であることを覚えていますか？つまり、コミュニティによって作成されたダッシュボードを追加できます！django-prometheusとよく連携する素晴らしいダッシュボードをandreynovikovが作成しています（https://grafana.com/grafana/dashboards/17658-django/）。それでは、このダッシュボードをGrafanaに追加する方法を探ってみましょう！

### データソースの追加

データソースはPrometheusから取得していることを覚えておいてください。追加しましょう！

- データソースに移動します
- データソースを追加するをクリックします
- Prometheusを選択し、これで最初のデータソースが作成されます。😁
- 接続にスクロールし、PrometheusサーバーのURLを `http://prometheus:9090` と入力します。これは、GrafanaのDockerコンテナからアクセスされるときのPrometheus Dockerコンテナのドメインです。
- 一番下までスクロールして、Save & Testをクリックします。緑のチェックマークが表示されれば（おそらく表示されるでしょう）、準備完了です！

### ダッシュボードの追加

さて、andreynovikovが作成したダッシュボードをGrafanaに追加します。さっそく始めましょう！

- ダッシュボードに移動します
- Create Dashboardをクリックします
- Import dashboardをクリックし、"Find and import dashboards"入力フィールドに希望のダッシュボードのURLを入力し、Loadをクリックします
- 作成したばかりのPrometheusデータソースをデータソースとして選択し、Importをクリックします。

これで、インポートしたダッシュボードが表示されます！
