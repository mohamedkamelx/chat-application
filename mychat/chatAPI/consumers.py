# chatAPI/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message, User
from user_reg.models import UserProfile
from channels.db import database_sync_to_async
from django.utils.timezone import now


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Check if user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'{self.chat_id}'
        
        await self.set_online(self.scope['user'])

        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def set_online(self, user):
        user_id = user.id
        UserProfile.objects.filter(user_id=user_id).update(is_online=True)
        return True

    @database_sync_to_async
    def set_offline(self, user):
        user_id = user.id
        UserProfile.objects.filter(user_id=user_id).update(
                is_online=False, 
                last_seen=now()
            )
        return True


    @database_sync_to_async
    def add_to_db(self, msg):
        try:
            text = msg['text']
            chat_id = msg['chat_id']
            sender_id = msg['sender']
            
            chat = Chat.objects.get(id=chat_id)
            sender = User.objects.get(id=sender_id)
            
            Message.objects.create(chat=chat, text=text, sender=sender)
            return True
        except Exception as e:
            print(f"Error saving message: {e}")
            return False

    async def disconnect(self, close_code):
        if hasattr(self, 'scope') and self.scope['user'].is_authenticated:
            await self.set_offline(self.scope['user'])
        
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            msg = json.loads(text_data)
            success = await self.add_to_db(msg)
            
            if success:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": 'handeler_method',
                        "message": msg
                    }
                )
            else:
                # Send error message back to client
                await self.send(text_data=json.dumps({
                    'error': 'Failed to save message'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except Exception as e:
            print(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': 'Server error'
            }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    async def handeler_method(self, event):
        try:
            msg = event['message']
            user = await self.get_user(msg['sender'])
            
            if user:
                msg['sender_username'] = str(user)
                await self.send(text_data=json.dumps({'message': msg}))
            else:
                print(f"User with ID {msg['sender']} not found")
        except Exception as e:
            print(f"Error in handeler_method: {e}")

#{"type":"message","chat_id":1,"room_code":"1","sender":1,"text":"s","time":"2025-07-04T01:11:52.800Z","read_by":[],"read":false}