from .models import User
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    last_seen = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username','id', 'last_seen', 'is_online']

    def get_last_seen(self, obj):
        return obj.profile.last_seen

    def get_is_online(self, obj):
        return obj.profile.is_online

