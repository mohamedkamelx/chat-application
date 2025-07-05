from django.contrib import admin
from .models import Chat, Group_pep, Message

# Inline messages inside Chat/Group admin
class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

# For basic Chat model
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_private']
    filter_horizontal = ('participate',)
    inlines = [MessageInline]

# For Group chat with name, code, admin
@admin.register(Group_pep)
class GroupPepAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'admin']
    filter_horizontal = ('participate',)
    inlines = [MessageInline]



from django.contrib import admin
from .models import Message, ReadMsg, Chat
from django.contrib.auth import get_user_model

User = get_user_model()

class ReadMsgInline(admin.TabularInline):
    model = ReadMsg
    extra = 1
    autocomplete_fields = ['user']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'text', 'time', 'read', 'seen_by']
    list_filter = ['read', 'time']
    search_fields = ['text', 'sender__username']
    inlines = [ReadMsgInline]

    def seen_by(self, obj):
        return ", ".join([
            f"{r.user.username} at {r.time.strftime('%Y-%m-%d %H:%M:%S')}" 
            for r in obj.read_group.all()
        ])
    seen_by.short_description = 'Seen By (with time)'
