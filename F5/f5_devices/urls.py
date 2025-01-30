# f5_devices/urls.py

from django.urls import path
from .views import get_device_list

urlpatterns = [
    path("device-list/", get_device_list, name="get_device_list"),
]
