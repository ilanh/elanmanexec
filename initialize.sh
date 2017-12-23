#!/bin/bash
python3 /code/portal/manage.py collectstatic --noinput
python3 /code/portal/manage.py makemigrations
python3 /code/portal/manage.py migrate --noinput
