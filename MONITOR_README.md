# Django Application Monitoring Setup

[日本語版はこちら](./MONITOR_README_ja.md)

This document explains how to set up monitoring for the Django application in the ft_transcendence project.

## Table of Contents

1. [Setting up django-prometheus](#setting-up-django-prometheus)
2. [Setting up Prometheus and Grafana with Docker Compose](#setting-up-prometheus-and-grafana-with-docker-compose)
3. [Adding Grafana Dashboards](#adding-grafana-dashboards)

## Setting up django-prometheus

[django-prometheus](https://github.com/korfuri/django-prometheus) is a Python library that exports monitoring metrics from Django applications to Prometheus.

### Installation

```bash
pip install django-prometheus
```

### Configuration

1. Add the following to `settings.py`:

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

2. Add the following to `urls.py`:

```python
urlpatterns = [
    ...
    path("prometheus/", include("django_prometheus.urls")),
]
```

This will make metrics available at the `/prometheus/metrics` endpoint.

## Setting up Prometheus and Grafana with Docker Compose

### Docker Compose Configuration

Create a `docker-compose.monitoring.yml` file with the following content:

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

### Prometheus Configuration

Create a `prometheus.yml` file with the following content:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: "django_app"
    metrics_path: "/prometheus/metrics"
    static_configs:
      - targets: ["host.docker.internal:8080"]
```

Note: Adjust the `targets` value to match the actual host and port of your Django application.

### Starting Docker Compose

```bash
docker-compose -f docker-compose.monitoring.yml up --build
```

This will make the following services available:

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

## Adding Grafana Dashboards

### Adding a Data Source

1. Log in to Grafana (default credentials: admin/admin)
2. Go to "Configuration" → "Data sources" in the left menu
3. Click "Add data source"
4. Select Prometheus
5. Set the following:
   - Name: Prometheus
   - URL: `http://prometheus:9090`
6. Click "Save & Test"

### Importing a Dashboard

1. Go to "Create" → "Import" in the left menu
2. Enter [Django Prometheus](https://grafana.com/grafana/dashboards/17658-django/) dashboard URL in "Import via grafana.com".
3. Click "Load"
4. Select Prometheus as the data source
5. Click "Import"

You should now have a dashboard displaying metrics from your Django application.

## Troubleshooting

- If metrics are not showing up, ensure that your Django application is running correctly and that the Prometheus configuration is correct.
- If Grafana fails to connect to the data source, check your network settings and ensure that the Prometheus container is reachable from the Grafana container.

## References

- [django-prometheus GitHub](https://github.com/korfuri/django-prometheus)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
