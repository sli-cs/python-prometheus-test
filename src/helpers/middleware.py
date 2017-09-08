from flask import request
from prometheus_client import Counter, Histogram, Gauge
import time
import sys

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['endpoint']
)

# app_build_info
app_name = 'my cool app'
revision = 'unknown'
try:
    with open('.git-revision') as f:
        revision = f.read().rstrip()
except IOError:
    print('Cannot read file .git-revision')

APP_VERSION = Gauge(
    'app_build_info', 'App Version Information',
    ['app', 'revision'],
)

APP_VERSION.labels(app_name, revision).set(1)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(resp_time)
    return response

def record_request_data(response):
    REQUEST_COUNT.labels(request.method, request.path,
            response.status_code).inc()
    return response

def setup_metrics(app):
    app.before_request(start_timer)
    # The order here matters since we want stop_timer
    # to be executed first
    app.after_request(record_request_data)
    app.after_request(stop_timer)
