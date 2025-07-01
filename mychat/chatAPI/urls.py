from django.urls import path
from . import views
urlpatterns = [
    path("home/",views.home,name='home') ,

    path("chat/",views.Chats.as_view(),name='chats') ,
    path("group/",views.Groups.as_view(),name='group') ,

    path("chat/<int:chat_id>",views.MessagesAPI.as_view(),name="chat"),
    path("chat-page/<int:chat_id>",views.messages,name="chat-page"),

    path("search/",views.SearchView.as_view(), name='search') ,
    path("group-join/",views.JoinGroupByCodeAPIView.as_view(), name='group-join') ,
]
