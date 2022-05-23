from django.urls import include, path
from rest_framework import routers

from foods.views import IngredientViewSet, TagViewSet
from foods.views import RecipeViewSet

router_ingredient = routers.DefaultRouter()
router_ingredient.register(r'', IngredientViewSet, basename='ingredient')

router_tag = routers.DefaultRouter()
router_tag.register(r'', TagViewSet, basename='tag')

router_recipe = routers.DefaultRouter()
router_recipe.register(r'', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('ingredients/', include(router_ingredient.urls)),
    path('tags/', include(router_tag.urls)),
    path('recipes/', include(router_recipe.urls)),
]
