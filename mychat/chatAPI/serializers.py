from rest_framework import serializers
from .models import Chat, Group_pep, Message
from user_reg.models import User
from django.shortcuts import get_object_or_404
import random
import string



class PrivateChatListSerializer(serializers.ModelSerializer):
    lastMessage = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    username_input = serializers.CharField(write_only=True, required=False)


    class Meta:
        model = Chat
        fields = ['id','username','lastMessage','unread','username_input','time']

    def get_unread(self,obj):
        user = self.context['request'].user
        return obj.message_set.filter(read=False).exclude(sender=user).count()
    
    def get_time(self,obj):
        return obj.last_msg_time
    
    def get_lastMessage(self,obj):
        last_msg = obj.message_set.order_by('-time').first()
        return last_msg.text if last_msg else None
    
    def get_username(self,obj):
        user = self.context['request'].user
        other_users = obj.participate.exclude(id=user.id).first().username
        return other_users
    
    def create(self,validated_data):
        print(validated_data)

        me = get_object_or_404(User, pk = self.context['request'].user.pk)
        user = get_object_or_404(User, username = validated_data.pop("username_input"))

        chat_exist_check = Chat.objects.filter(is_private=True, participate=me).filter(participate=user).first()
        if chat_exist_check:
            return chat_exist_check
        chat = Chat.objects.create(is_private=True)
        chat.participate.set([me, user])
        chat.save()

        return chat
    

class GroupSerializer(serializers.ModelSerializer):
    lastMessage = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    members = serializers.ListField(child=serializers.CharField(), write_only=True)
    unread = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Group_pep
        fields = ['id','name','members','lastMessage','unread','time']

    def get_time(self,obj):
        return obj.last_msg_time
    
    def get_lastMessage(self,obj):
        last_msg = obj.message_set.order_by('-time').first()
        return last_msg.text if last_msg else None
    
    def get_unread(self,obj):
        user = self.context['request'].user
        return obj.message_set.exclude(sender=user).exclude(read_group__user=user).count()
        
    def create(self, validated_data):
        me = get_object_or_404(User, pk = self.context['request'].user.pk)
        name = validated_data.pop("name")
        group = Group_pep.objects.create(name=name,code=generate_random_code(),admin=me,is_private=False)
        usernames = validated_data.pop('members')
        users = list(User.objects.filter(username__in=usernames)) + [me]
        group.participate.set(users)
        group.save()

        return group

class MessageSerializer(serializers.ModelSerializer):
    read_by = serializers.SerializerMethodField(read_only=True)
    sendername = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['sender','time','text','read_by','read',"sendername"]

    def get_sendername(self, obj):
        return obj.sender.username
    def get_read_by(self, obj):
        read_by={}
        for r in obj.read_group.all():
            read_by[r.user.username]=r.time
        return read_by


    
class MyChat(serializers.ModelSerializer):
    
    chatname = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, source='message_set')
    myid = serializers.SerializerMethodField()
    lastseen = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id','chatname', 'messages','myid','is_online','lastseen']

    def get_chatname(self, obj):
        user = self.context['request'].user
        if obj.is_private:
            name = obj.participate.exclude(id=user.id).first().username
        else:
            group = Group_pep.objects.filter(id=obj.id).first()
            name = group.name if group else "Unnamed Group"
        return name
    def get_myid(self,obj):
        return self.context['request'].user.id
    def get_is_online(self,obj):
        user = self.context['request'].user        
        return obj.participate.exclude(id=user.id).first().profile.is_online
    def get_lastseen(self,obj):
        user = self.context['request'].user 
        return obj.participate.exclude(id=user.id).first().profile.last_seen


def generate_random_code(length=10):
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choices(characters, k=length))