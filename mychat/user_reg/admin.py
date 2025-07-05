from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_seen', 'is_online')
    search_fields = ('user__username',)
    list_filter = ('is_online',)
