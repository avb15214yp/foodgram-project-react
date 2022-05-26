from django.urls import include, path
from rest_framework import routers

from users.views import UserListCreateViewSet

router = routers.DefaultRouter()
router.register(r'', UserListCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
