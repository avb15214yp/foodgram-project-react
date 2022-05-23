from django.urls import path, include

from foods.views import SubscriptionViewSet


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/subscriptions/',
         SubscriptionViewSet.as_view({'post': 'create'})),
    path('users/', include('users.urls')),
    path('', include('foods.urls')),
]
