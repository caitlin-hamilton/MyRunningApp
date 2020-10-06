import os
import django

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'my_running_app.settings'
    django.setup()
    from my_runs.views import create_run_entry
    create_run_entry()

