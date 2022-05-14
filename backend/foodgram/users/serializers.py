
from rest_framework import serializers

from users.models import User


class UserSerializerList(serializers.HyperlinkedModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [ 'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']
    
    def get_is_subscribed(self, obj):
        return True

class UserSerializerCreate(serializers.HyperlinkedModelSerializer):
        
    class Meta:
        model = User
        fields = [ 'email', 'id', 'username', 'first_name', 'last_name']
