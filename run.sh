#!/usr/bin/env bash
sleep 5
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py shell < createsuperuser.py
python3 manage.py runserver 0.0.0.0:8000
