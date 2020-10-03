from django.apps import AppConfig


class MyRunsConfig(AppConfig):
    name = 'my_runs'


#python manage.py migrate --run-syncdb
