from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer

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
        elif self.action == 'set_password':
            return SetPasswordSerializer
        return UserSerializerList

    def get_instance(self):
        return self.request.user

    @action(["get",], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)