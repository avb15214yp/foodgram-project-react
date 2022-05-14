from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from api.mixins import ListCreateViewSet
from users.serializers import UserSerializerList, UserSerializerCreate
from users.permissions import UserListCreatePermission

User = get_user_model()

class UserListCreateViewSet(ListCreateViewSet):    
    queryset = User.objects.all()
    permission_classes = (UserListCreatePermission,)

    def get_serializer_class(self):
        if self.action == 'create':            
            return UserSerializerCreate
        return UserSerializerList

    def get_instance(self):
        return self.request.user

    @action(["get",], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)