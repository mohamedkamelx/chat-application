from django.urls import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/file/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]