#!/bin/bash

set -o errexit
set -o nounset

celery worker -A worker.celery_app --loglevel=info