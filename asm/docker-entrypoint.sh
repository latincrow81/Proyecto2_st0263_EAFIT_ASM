#!/bin/sh

set -e

gunicorn --enable-stdio-inheritance --bind 0.0.0.0:80 --reload wsgi:app
