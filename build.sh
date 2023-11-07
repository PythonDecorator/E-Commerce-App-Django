#!/usr/bin/env bash
# exit on error
set -o errexit

pip install poetry==1.5.1

python -m poetry install

python manage.py collectstatic --no-input
python manage.py migrate
