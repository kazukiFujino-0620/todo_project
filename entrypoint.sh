#!/bin/bash
set -e

until python manage.py runserver 0.0.0.0:8000; do
  echo "Django server failed to start. Retrying in 5 seconds..."
  sleep 5
done