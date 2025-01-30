from django.urls import re_path
from websockets.consumers import DeviceStatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/device-status/$", DeviceStatusConsumer.as_asgi()),
]
