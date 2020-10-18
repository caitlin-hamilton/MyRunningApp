from django.urls import path, include
from django.contrib import admin


# from my_runs.views import run, index

app_name = 'my_runs'

from rest_framework import routers                    # add this
from my_runs import views                            # add this

router = routers.DefaultRouter()                      # add this
router.register(r'runs', views.RunView, 'runs')
router.register(r'splits', views.SplitView, 'splits')

urlpatterns = [
    # path('<int:run_id>/', run, name='run'),
    # path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]