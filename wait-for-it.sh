#!/usr/bin/env bash
# wait-for-it.sh - Скрипт для ожидания доступности сервиса по IP/порту

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

while ! nc -z "$host" "$port"; do
  echo "Ждем доступности $host:$port..."
  sleep 2
done

echo "$host:$port доступен, запускаем тесты..."
exec $cmd