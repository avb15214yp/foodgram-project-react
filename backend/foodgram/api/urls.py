from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include('users.urls')),
    path('', include('foods.urls')),
]