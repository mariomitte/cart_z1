release: python manage.py migrate
web: gunicorn settings.wsgi:application --log-file -
worker: celery -A settings.celery worker --without-gossip --without-mingle --without-heartbeat -O fair -P gevent -l INFO
