#!/bin/bash

python manage.py flush
python manage.py makemigrations
python manage.py migrate
python manage.py add_notification_types
python manage.py add_tax
python manage.py add_example_invoice
