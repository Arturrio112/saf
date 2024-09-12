from django.urls import path
from .views import metrics, sensors, sensor_types

urlpatterns = [
    path('metrics/', metrics, name='metrics'),
    path('sensors/', sensors, name='sensors'),
    path('types/', sensor_types, name='types'),
]
