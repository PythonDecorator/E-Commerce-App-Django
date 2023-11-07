#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing the latest version of poetry..."

pip install --upgrade pip

pip install poetry==1.5.0

python -m poetry install

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py  wait_for_db
python manage.py migrate
