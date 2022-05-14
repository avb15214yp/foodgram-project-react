from rest_framework import permissions

class UserListCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.method == 'POST':
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj == request.user 
