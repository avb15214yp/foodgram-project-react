from django.urls import include, path
from djoser.views import UserViewSet
from users.views import UserListCreateViewSet
from rest_framework import routers

# urlpatterns = [
#     # path('', include('djoser.urls')),
#     path('users/', UserViewSetCustom.as_view({'get': 'list'}), name="user_list"),
# ]

router = routers.DefaultRouter()
router.register(r'users', UserListCreateViewSet)

urlpatterns = [
    # path('users/me/', UserListCreateViewSet, name='me'),
    path('', include(router.urls)),    
]	