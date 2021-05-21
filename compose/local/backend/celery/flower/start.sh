#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A worker.celery_app inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

flower \
    --app=worker.celery_app \
    --broker="${CELERY_BROKER_URL}"