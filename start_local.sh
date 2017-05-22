#!/bin/bash

# Set environment options to exit immediately if a non-zero status code
# appears from a command or within a pipe
set -o errexit
set -o pipefail

# Run migrations
./manage.py makemigrations
./manage.py migrate --noinput

# Run application
python manage.py runserver
