#!/bin/bash
# Development server startup script

set -e

echo "Starting MetaTasks development server..."

# Check if database is ready
python manage.py check --deploy || true

# Run migrations
python manage.py migrate --noinput

# Start development server
python manage.py runserver 0.0.0.0:8000
