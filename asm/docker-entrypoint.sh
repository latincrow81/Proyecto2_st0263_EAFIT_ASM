#!/bin/sh

set -e

gunicorn --enable-stdio-inheritance --bind 0.0.0.0:8080 --reload wsgi:app
