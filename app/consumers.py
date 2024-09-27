import json
from channels.generic.websocket import AsyncWebsocketConsumer


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceita a conexão WebSocket
        self.room_name = "chat_room"  # Nome do grupo, você pode usar algo dinâmico
        self.room_group_name = f'chat_{self.room_name}'

        # Armazenar o usuário do escopo, se presente
        self.user = self.scope['user']  # Acessando o usuário autenticado do escopo

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
                'type': 'chat_message',
                'message': message,
                'userId':str(self.user.id), 
                'sender': self.user.username if self.user.is_authenticated else 'Anonymous',  # Envia o nome do usuário
                'channel_name': self.channel_name  # Envia o canal do remetente
            }
        )
        room_group_name = f'notification{str(self.user.id)}'
        print("limites",room_group_name)

                # Envia a mensagem para o grupo de chat, incluindo o nome do usuário
        await self.channel_layer.group_send(
            room_group_name,
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
            'userfd': sender,  # Inclui o nome do usuário na mensagem
            'message': message,
            'Notificacao':"Testando",
            "NNNN":"34"
        }))


    async def chat_message(self, event):
        # Recebe a mensagem do grupo e envia para o WebSocket, exceto para o remetente
        message = event['message']
        sender = event['sender']
        
        # Envia a mensagem apenas se não for do mesmo remetente
        await self.send(text_data=json.dumps({
            'userfd': sender,  # Inclui o nome do usuário na mensagem
            'message': message
        }))



class Notifications(AsyncWebsocketConsumer):
    async def connect(self):
        # Aceita a conexão WebSocket
        self.room_name = "chat_room"  # Nome do grupo, você pode usar algo dinâmico

        # Armazenar o usuário do escopo, se presente
        self.user = self.scope['user']  # Acessando o usuário autenticado do escopo
        self.room_group_name = f'notification{str(self.user.id)}'

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
        print("Envia a " + self.room_group_name)
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
            'userfd': sender,  # Inclui o nome do usuário na mensagem
            'message': message,
            "Notificacao":"Testando",
            "Testada":"342"
        }))

