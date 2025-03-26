# almacenes/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from almacenes.consumer import NotificacionConsumer  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacenes.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
       URLRouter([
            path('ws/notificaciones/', NotificacionConsumer.as_asgi()),
        ])
    ),
})
