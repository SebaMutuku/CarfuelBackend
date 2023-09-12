#!/bin/bash

echo "***** Building the project *****"
python3 -m pip install -r requirements.txt
echo "***** Make Migration *****"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
echo "***** Collecting Static *****"
python3 manage.py collectstatic --noinput --clear