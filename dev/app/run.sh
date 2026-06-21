#!/bin/bash

python manage.py migrate
gunicorn --bind=0.0.0.0:8000 -w 8 --timeout=1800 smartthingsbridge.wsgi

