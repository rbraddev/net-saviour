#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

edgedb_ready() {
python << END
import sys

from edgedb import connect

from app.config import get_settings

settings = get_settings()

try:
    conn = connect(
        host=settings.EDGEDB_HOST,
        database=settings.EDGEDB_DB,
        user=settings.EDGEDB_USER,
        password=settings.EDGEDB_PASSWORD,
    )
    conn.execute("SELECT 1")
except Exception as e:
    print(e)
    sys.exit(-1)
sys.exit(0)

END
}

until edgedb_ready; do
  >&2 echo 'Waiting for EdgeDB to become available...'
  sleep 1
done
>&2 echo 'EdgeDB is available'



exec "$@"