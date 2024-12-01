from django.urls import path
from . import consumers
import json
from channels.generic.websocket import AsyncWebsocketConsumer

websocket_urlpatterns = [
    path('ws/chat/', consumers.NotificationConsumer.as_asgi()),
]

# Honestly not sure if this is backend or frontend