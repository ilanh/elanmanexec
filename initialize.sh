#!/bin/bash
# Initialize Django project
python3 /code/portal/manage.py collectstatic --noinput
python3 /code/portal/manage.py makemigrations
python3 /code/portal/manage.py migrate --noinput
