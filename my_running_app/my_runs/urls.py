from django.urls import path
from django.contrib import admin


from my_runs.views import run, index

app_name = 'my_runs'

urlpatterns = [
    path('<int:run_id>/', run, name='run'),
    path('', index, name='index'),
    #my_runs
    path('admin/', admin.site.urls),
]