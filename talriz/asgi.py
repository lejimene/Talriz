"""
ASGI config for talriz project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from talriz import routing 

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talriz.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(  
#         URLRouter(
#             routing.websocket_urlpatterns  
#         )
#     ),
# })

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from django.contrib.auth.middleware import AuthenticationMiddleware
from channels.routing import URLRouter
from . import routing





os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talriz.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthenticationMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
