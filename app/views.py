from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 
 
from .utils import sendWebsocketNotification
class Index(APIView):
    def get(self, request):
        user = request.user  
        content = {'message': 'Hello, World!'}
        sendWebsocketNotification(user, content)
        return Response(content, status=status.HTTP_200_OK)


#Notificações crud

class notificacoesView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content, status=status.HTTP_200_OK)

class GrupoView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content, status=status.HTTP_200_OK)

class MensagemView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content, status=status.HTTP_200_OK)





#GrupoCrud