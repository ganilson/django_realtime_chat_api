import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
# from .models import Room
class Messages(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceita a conexão WebSocket
        # self.room_name = "chat_room" 
        self.senderId = self.scope["url_route"]["kwargs"]["senderId"]
        self.receiverId = self.scope["url_route"]["kwargs"]["receiverId"]
        print("SENDER ID:", self.senderId)
        print("RECEIVER ID:", self.receiverId)
        self.user = self.scope['user'] 
        self.room_group_name = f'chat_between_{self.senderId}_{self.receiverId}'
        print(self.room_group_name)

        # Junta-se ao grupo de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Sai do grupo de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recebe mensagens do WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Received message: " + message)
        print("User:", str(self.user.id))  # Imprime o usuário

                 # Envia a mensagem para o grupo de chat, incluindo o nome do usuário
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendWithId',
                'message': message,
                'senderId':str(self.user.id), 
                'sender': self.user.username if self.user.is_authenticated else 'Anonymous',  # Envia o nome do usuário
                'channel_name': self.channel_name  # Envia o canal do remetente
            }
        )


    async def sendWithId(self, event):
        # Recebe a mensagem do grupo e envia para o WebSocket, exceto para o remetente
        message = event['message']
        sender = event['sender']
        senderId = event['senderId']
        
        # Envia a mensagem apenas se não for do mesmo remetente
        await self.send(text_data=json.dumps({
            'senderId': senderId,  # Inclui o nome do usuário na mensagem
            'sender': sender,  # Inclui o nome do usuário na mensagem
            'message': message,
         }))


