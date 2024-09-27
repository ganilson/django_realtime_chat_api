# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from app.middlewares import JWTAuthMiddleware
from django.urls import path
from app.urls import websocket_urlpatterns
# from app import consumers  # Importe os consumers do seu app
import django
django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
applicationServer = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})


application = JWTAuthMiddleware(
    inner=applicationServer,
    protected_paths=["/app/"]
)

