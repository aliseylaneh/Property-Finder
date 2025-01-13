python manage.py migrate
python manage.py search_index --rebuild -f
python manage.py createsuperuser --username admin --email admin@example.com --noinput
python manage.py collectstatic --noinput
gunicorn --workers 4 --bind 0.0.0.0:8000 config.django.base:application
