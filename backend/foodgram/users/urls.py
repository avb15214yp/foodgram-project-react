from django.urls import include, path
from users.views import UserListCreateViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', UserListCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
