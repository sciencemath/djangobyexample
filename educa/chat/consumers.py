import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.user = self.scope['user']
    self.id = self.scope['url_route']['kwargs']['course_id']
    self.room_group_name = f'chat_{self.id}'
    await self.channel_layer.group_add(
      self.room_group_name, self.channel_name
    )
    # async_to_sync(self.channel_layer.group_add)(
    #   self.room_group_name, self.channel_name
    # )
    await self.accept()
  
  async def persist_message(self, message):
    await Message.objects.acreate(
      user=self.user, course_id=self.id, content=message
    )

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name, self.channel_name
    )
    # async_to_sync(self.channel_layer.group_discard)(
    #   self.room_group_name, self.channel_name
    # )

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    now = timezone.now()
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'user': self.user.username,
        'datetime': now.isoformat(),
      }
    )
    # sanatize message with nh3 package
    await self.persist_message(message)
    # async_to_sync(self.channel_layer.group_send)(
    #   self.room_group_name,
    #   {
    #     'type': 'chat_message',
    #     'message': message,
    #     'user': self.user.username,
    #     'datetime': now.isoformat(),
    #   }
    # )
    # self.send(text_data=json.dumps({'message': message}))

  async def chat_message(self, event):
    await self.send(text_data=json.dumps(event))