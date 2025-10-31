#!/bin/bash

# Azure App Service startup script
echo "Starting F1 Betting Pool..."

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput --clear

# Start Gunicorn
exec gunicorn f1betting.wsgi:application \
    --bind=0.0.0.0:${PORT:-8000} \
    --workers=4 \
    --timeout=120 \
    --access-logfile=- \
    --error-logfile=-
