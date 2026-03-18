#!/usr/bin/env bash
# Render build script — runs on every deploy
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files into STATIC_ROOT
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate
