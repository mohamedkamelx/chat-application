from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .models import Chat, Group_pep, User, Message
from . import serializers
from rest_framework.response import Response
from rest_framework import permissions

# Create your views here.


@login_required(login_url='/user/login/')
def home(request):
    return render(request,'chat_app_homepage.html')



class Chats(ListCreateAPIView):
    serializer_class = serializers.PrivateChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(is_private=True, participate=self.request.user).prefetch_related(
                    'participate',
                    'message_set',
                ).order_by('-message_set__time')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    


class Groups(ListCreateAPIView):
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        return Group_pep.objects.filter(participate=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class JoinGroupByCodeAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        user = request.user

        if not code:
            return Response({"detail": "Group code is required."}, status=400)

        group = Group_pep.objects.filter(code=code).first()
        if not group:
            return Response({"detail": "Group not found."}, status=404)

        if user in group.participate.all():
            return Response({
                "id": group.id,
                "name": group.name,
                "detail": "You are already a member of this group."
            }, status=200)

        group.participate.add(user)

        return Response({
            "id": group.id,
            "name": group.name
        }, status=200)



class SearchView(APIView):
    def get(self, request):
        q=request.query_params.get("q")
        if not q:
            return Response({"detail": "Group code is required."}, status=400)
        results = User.objects.filter(username__icontains=q).exclude(username=request.user.username).values('id', 'username')

        return Response(results, status=200)
        

class MessagesAPI(APIView):
    def get(self,request, chat_id):
        mychat = Chat.objects.get(id=chat_id)
        messages = Message.objects.filter(chat=mychat)
        serializer = serializers.MessageSerializer(messages,many=True, context={'request': request})
        Message.objects.filter(chat=mychat).update(read=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = serializers.MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True}, status=200)
        else:return Response({"success":False}, status=200)



@login_required(login_url='/user/login/')
def messages(request):
    return render(request,'chat_app_homepage.html')
