from rest_framework import permissions


class CAuthUserUDOwnerRAnyPermisson(permissions.BasePermission):

    def __init__(self, field_owner_name='author'):
        self.field_owner_name = field_owner_name

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, self.field_owner_name) == request.user


class CAuthUserDLOwnerPermisson(permissions.BasePermission):

    def __init__(self, field_owner_name='author'):
        self.field_owner_name = field_owner_name

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return getattr(obj, self.field_owner_name) == request.user
