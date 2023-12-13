#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

echo "***** Make Migration *****"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

python manage.py collectstatic --no-input
python manage.py migrate