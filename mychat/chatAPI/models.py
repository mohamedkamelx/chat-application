from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Chat(models.Model):
    participate = models.ManyToManyField(User,related_name="chats", blank=True)
    is_private = models.BooleanField(default=True)

class Group_pep(Chat):
    code = models.CharField(max_length=20,unique=True, blank=True)
    name = models.CharField(max_length=20)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="message_set")
    time = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    read = models.BooleanField(default=False)


class ReadMsg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="read_group")
    time = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        unique_together = ('user', 'message')  
