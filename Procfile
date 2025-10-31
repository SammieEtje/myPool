web: gunicorn f1betting.wsgi:application --bind 0.0.0.0:$PORT --workers 4
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
