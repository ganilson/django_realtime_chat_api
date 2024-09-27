from django.contrib.auth import authenticate
from django.http import JsonResponse
from .utils import generate_jwt
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            token = generate_jwt(user)
            return JsonResponse({'token': token}, status=200)
        else:
            return JsonResponse({'error': 'Credenciais invelidas por favor, verifique o seu email e password!'}, status=400)
