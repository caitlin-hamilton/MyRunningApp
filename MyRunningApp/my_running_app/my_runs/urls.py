from django.urls import path
from django.contrib import admin


from . import views

app_name = 'my_runs'

urlpatterns = [
    path('<int:run_id>/', views.run, name='run'),
    path('admin/', admin.site.urls),
]