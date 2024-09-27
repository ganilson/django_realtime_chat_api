from django.urls import path
from .views import *
from .consumers import *
from .login import login_view
from .middlewares import  JWTAuthMiddleware,JWTAuthMiddlewareHTTP
from .message import Messages
urlpatterns = [
    path('index/',JWTAuthMiddlewareHTTP(Index.as_view()), name="index"), 
     # path('notificacoes',login_view, name="login"), 
    # path('mensagens/<str:senderId>/<str:receiverId>',login_view, name="mensagens"), 
    # path('grupos/<str:senderId>/<str:receiverId>',login_view, name="mensagens"), 

    ]

websocket_urlpatterns = [
    path("app/", JWTAuthMiddleware(YourConsumer.as_asgi())),
    path("app/notificacao/", JWTAuthMiddleware(Notifications.as_asgi())),
    path("app/mensagens/<int:senderId>/<int:receiverId>/", JWTAuthMiddleware(Messages.as_asgi())),
    path("app/notificacao/", JWTAuthMiddleware(Notifications.as_asgi())),
    # Adicione mais rotas WebSocket aqui...
]