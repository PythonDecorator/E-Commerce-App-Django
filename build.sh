#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing the latest version of poetry..."

pip install --upgrade pip

pip install poetry==1.7.0

python -m poetry install

python -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
