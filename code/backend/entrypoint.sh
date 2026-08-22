#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Start the application
echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
