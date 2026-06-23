#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Applying database migrations"
python manage.py migrate

echo "Starting server"
gunicorn ESGBack.wsgi:application --bind 0.0.0.0:8000