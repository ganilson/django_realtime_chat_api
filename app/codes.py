# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f'user_{self.user.id}'

            # Adiciona o usuário ao grupo
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Enviar notificações não lidas ao conectar
            notifications = await self.get_notifications()
            await self.send(text_data=json.dumps({
                'type': 'initial_notifications',
                'notifications': notifications
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'save_item':
            # Salvar item no banco de dados (a lógica para salvar o item deve ser implementada aqui)
            item_name = data.get('item_name')
            item_description = data.get('item_description')
            await self.save_item(item_name, item_description)

            # Enviar notificação ao usuário
            notification = await self.create_notification(f'Novo item "{item_name}" foi salvo!')
            await self.send_notification(notification)

    async def send_notification(self, notification):
        await self.channel_layer.group_send(self.group_name, {
            'type': 'notify_user',
            'notification': notification
        })

    async def notify_user(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': notification
        }))

    async def save_item(self, name, description):
        # Lógica para salvar o item no banco de dados (implementação a ser definida)
        pass

    async def create_notification(self, message):
        # Criar e salvar a notificação no banco de dados
        notification = await database_sync_to_async(Notification.objects.create)(
            user=self.user,
            message=message
        )
        return {
            'id': notification.id,
            'message': notification.message,
            'timestamp': str(notification.timestamp),
            'read': notification.read
        }

    async def get_notifications(self):
        # Recuperar notificações não lidas do banco de dados
        notifications = await database_sync_to_async(
            Notification.objects.filter(user=self.user, read=False).order_by('-timestamp').values
        )()
        return list(notifications)
