gunicorn \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --capture-output \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  core.project.wsgi:application