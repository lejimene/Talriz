from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/', consumers.NotificationConsumer.as_asgi())
]

# Honestly not sure if this is backend or frontend z