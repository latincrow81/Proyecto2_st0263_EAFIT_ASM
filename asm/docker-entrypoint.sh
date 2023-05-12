#!/bin/sh

set -e

gunicorn --enable-stdio-inheritance --bind 0.0.0.0:5000 --reload wsgi:app
