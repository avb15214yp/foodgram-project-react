from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializerList(serializers.HyperlinkedModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        user = request.user
        if not bool(user and user.is_authenticated):
            return False
        return obj.following.filter(user=user).exists()


class UserSerializerCreate(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']
