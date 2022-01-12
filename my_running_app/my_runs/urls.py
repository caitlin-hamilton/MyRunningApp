from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from my_runs import views

app_name = 'my_runs'

router = routers.DefaultRouter()
router.register(r'runs', views.RunView, 'runs')
router.register(r'splits', views.SplitView, 'splits')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]