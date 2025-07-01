from channels.generic.websocket import AsyncWebsocketConsumer

class Chat(AsyncWebsocketConsumer):
    async def connect(self):


        
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        pass