#!/bin/bash

# Set environment options to exit immediately if a non-zero status code
# appears from a command or within a pipe
set -o errexit
set -o pipefail

./manage.py collectstatic --noinput

# Run migrations
./manage.py makemigrations
./manage.py migrate --noinput
./manage.py createinitialrevisions

# Run application
gunicorn -w 2 customer_data.wsgi:application
