  
#!/bin/sh

echo "Waiting for EdgeDB..."

while ! nc -z nsav-db 5656; do
  sleep 0.1
done

echo "EdgeDB started"

exec "$@"