#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install



python manage.py migrate --fake admin zero
python manage.py migrate CarfuApp zero

python manage.py makemigrations
python manage.py migrate --run-syncdb

python manage.py collectstatic --no-input
