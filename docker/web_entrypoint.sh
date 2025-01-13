python manage.py migrate
python manage.py search_index --rebuild
python manage.py runserver
#gunicorn config.wsgi:application --workers=5 -b 0.0.0.0:8000