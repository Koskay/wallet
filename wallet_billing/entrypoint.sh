#!/bin/sh
# Применение миграций
python manage.py migrate

# Загрузка фикстур в определенном порядке
python manage.py loaddata users.json wallets.json

gunicorn \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --capture-output \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  core.project.wsgi:application