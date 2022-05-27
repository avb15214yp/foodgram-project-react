from django.urls import include, path
from rest_framework import routers

from foods.views import (IngredientViewSet, RecipeViewSet, SubscriptionViewSet,
                         TagViewSet)

router_ingredient = routers.DefaultRouter()
router_ingredient.register(r'', IngredientViewSet, basename='ingredient')

router_tag = routers.DefaultRouter()
router_tag.register(r'', TagViewSet, basename='tag')

router_recipe = routers.DefaultRouter()
router_recipe.register(r'', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'create'})),
    path('users/<int:id>/subscribe/',
         SubscriptionViewSet.as_view({'delete': 'delete'})),
    path('users/', include('users.urls')),
    path('ingredients/', include(router_ingredient.urls)),
    path('tags/', include(router_tag.urls)),
    path('recipes/', include(router_recipe.urls)),
]
