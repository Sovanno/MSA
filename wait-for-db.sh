#!/bin/sh
# wait-for-db.sh
set -e

host="$1"
shift

echo "Waiting for database $host..."
until pg_isready -h "$host" -p 5432; do
  sleep 2
done

# Запускаем миграции перед стартом приложения
if [ "$1" = "alembic" ]; then
  echo "Running Alembic migrations..."
  shift
  exec alembic upgrade head
fi

# Запускаем команду приложения
exec "$@"
