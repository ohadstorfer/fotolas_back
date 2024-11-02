#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Run database migrations
python manage.py migrate --noinput

# Collect static files without prompting
python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn --workers 2 myproj.wsgi:application --bind 0.0.0.0:8080