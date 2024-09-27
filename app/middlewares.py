import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json 



@database_sync_to_async
def get_user_from_jwt(token):
    User = get_user_model()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None

def get_token_from_scope(scope):
    """Extrai o token JWT do cabeçalho ou query string do WebSocket ou HTTP."""
    headers = dict(scope["headers"])
    token = None
    
    # Extração do token do cabeçalho Authorization
    if b"authorization" in headers:
        auth_header = headers[b"authorization"].decode("utf-8")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    # Ou pegar da query string (se for passado dessa forma)
    query_string = scope.get("query_string", b"").decode("utf-8")
    if not token and "token=" in query_string:
        token = query_string.split("token=")[1].split("&")[0]

    return token


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner, protected_paths=None):
        self.protected_paths = protected_paths or []
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        # Verifique se o caminho atual deve ser protegido
        if self.is_protected_path(scope['path']):
            token = get_token_from_scope(scope)
            print("Token extraído:", token)  # Log do token extraído
            
            if token:
                user = await get_user_from_jwt(token)
                if user is not None:
                    scope['user'] = user
                else:
                    await self.send_json_response(send, {
                        "error": "Token inválido ou expirado.",
                        "message": "Por favor, verifique seu token e tente novamente."
                    }, 401, scope)
                    return  # Finaliza o processamento aqui
            else:
                await self.send_json_response(send, {
                    "error": "Token não fornecido.",
                    "message": "Um token é necessário para se conectar. Adicione o token ao cabeçalho Authorization."
                }, 401, scope)
                return 

        await super().__call__(scope, receive, send)

    def is_protected_path(self, path):
        """Verifica se o caminho está na lista de caminhos protegidos."""
        return any(path.startswith(protected_path) for protected_path in self.protected_paths)

    async def send_json_response(self, send, response_data, status, scope):
        """Envia uma resposta JSON ao cliente."""
        response_body = json.dumps(response_data).encode('utf-8')


        if scope['type'] == 'http':
            print("HTTP")
            response = {
                'type': 'http.response.start',
                'status': status,
                'headers': [(b'content-type', b'application/json')],
            }
            await send(response)  
            await send({
                'type': 'http.response.body',
                'body': response_body,
            })
        elif scope['type'] == 'websocket':
 
            await send({
                'type': 'websocket.close',  
                'code': 4000,  
            })
            # Envia a resposta JSON como mensagem antes de fechar
            await send({
                'type': 'websocket.send',
                'text': response_body.decode('utf-8'),
            })
        else:
 
            raise ValueError("Tipo de conexão desconhecido: {}".format(scope['type']))
        
from django.utils.deprecation import MiddlewareMixin
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

class JWTAuthMiddlewareHTTP(MiddlewareMixin):
    def process_request(self, request):
        # Extrair token JWT do cabeçalho Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get('user_id')
                User = get_user_model()
                user = User.objects.get(id=user_id)
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
                return JsonResponse({"error": "Token inválido ou expirado."}, status=401)
        else:
            request.user = None
