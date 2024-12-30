import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user = self.scope['user']
#         self.id = self.scope['url_route']['kwargs']['course_id']
#         self.room_group_name = f'chat_{self.id}'
#         # присоединиться к группе чат-комнаты
#         async_to_sync(self.channel_layer.group_add)(
#         self.room_group_name,
#         self.channel_name
#         )
#         # принять соединение
#         self.accept()

#     def disconnect(self, close_code):
#         # покинуть группу чат-комнаты
#         async_to_sync(self.channel_layer.group_discard)(
#         self.room_group_name,
#         self.channel_name
#         )
#     # получить сообщение из веб-сокета
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         now = timezone.now()
#         # отправить сообщение в группу чат-комнаты
#         async_to_sync(self.channel_layer.group_send)(
#         self.room_group_name,
#         {
#         'type': 'chat_message',
#         'message': message,
#         'user': self.user.username,
#         'datetime': now.isoformat(),
#         })

#     # получить сообщение из группы чат-комнаты
#     def chat_message(self, event):
#         # отправить сообщение в веб-сокет
#         self.send(text_data=json.dumps(event))

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         # принять соединение
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     # получить сообщение из WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         # отправить сообщение в WebSocket
#         self.send(text_data=json.dumps({'message': message}))