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

# For individual message model (optional)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'text', 'time', 'read']
    list_filter = ['read', 'time']
    search_fields = ['text', 'sender__username']
