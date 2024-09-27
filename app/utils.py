import jwt
from datetime import datetime, timedelta
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

def generate_jwt(user):
    """
    Função para gerar um token JWT para o usuário autenticado.
    """
    
    payload = {
        'user_id': str(user.id), #Converter para string por ser do tipo UUID!!!
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'exp': datetime.now() + settings.JWT_EXPIRATION_DELTA,  # Definindo o tempo de expiração
    }
    print(payload)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    """
    Função para verificar e decodificar o token JWT.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido


def sendWebsocketNotification(user, content):
    try:
        room_group_name = f'notification{str(user.id)}'
        # Envia a notificação para o grupo WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'sendWithId',  # Nome do método que processa a mensagem no WebSocket
                'message': content['message'],
                'senderId': str(user.id), 
                'sender': user.username if user.is_authenticated else 'Anonymous'
            }
        )
        print(f'Notification sended to user: {user.username}')
    except:
        return JsonResponse({"error": "Token inválido ou expirado."}, status=401)
