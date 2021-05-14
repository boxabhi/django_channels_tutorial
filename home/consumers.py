from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login
class TestConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.user = self.scope["user"]
        print(vars(self.user))
        print(vars(self))
        self.send(text_data=json.dumps({'status' : 'connected from django channels'}))
        
    
    
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status' : 'we got you'}))


    def disconnect(self , *args, **kwargs):
        print('disconnected')
    
    
    def send_notification(self , event):
        print('send notification')
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload' : data}))
        
        print('send notification')



class NewConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.room_name = 'new_consumer'
        self.room_group_name = "new_consumer_group"
        
        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        self.user = self.scope["user"]
        print(self.user)
        await self.send(text_data=json.dumps({'status' : 'connected from new async json consumer'}))
        
        
    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'status' : 'we got you'}))


    async def disconnect(self , *args, **kwargs):
        await print('disconnected')
    
    async  def send_notification(self , event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'payload' : data}))
        
    
    
    