from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=False)),

    path("home/",views.home,name='home') ,

    path("chat/",views.Chats.as_view(),name='chats') ,
    path("group/",views.Groups.as_view(),name='group') ,

    path("chat/<int:chat_id>",views.MessagesAPI.as_view(),name="chat"),
    path("chat-web/<int:chat_id>",views.messages,name="chat-web"),
    path("group/<int:chat_id>",views.MessagesAPI.as_view(),name='group') ,

    path("search/",views.SearchView.as_view(), name='search') ,
    path("group-join/",views.JoinGroupByCodeAPIView.as_view(), name='group-join') ,
]
