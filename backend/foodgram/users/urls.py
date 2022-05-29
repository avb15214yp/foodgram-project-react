from django.urls import include, path
from rest_framework import routers

from foods.views import SubscriptionViewSet
from users.views import UserListCreateViewSet

router = routers.DefaultRouter()
router.register(r'users', UserListCreateViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:id>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'create', 'delete': 'delete'})),
    path('users/subscriptions/',
         SubscriptionViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
