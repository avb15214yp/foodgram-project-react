from django.urls import include, path
from rest_framework import routers

from foods.views import IngredientListViewSet, TagListViewSet
from foods.views import RecipeListCreateViewSet

router_ingredient = routers.DefaultRouter()
router_ingredient.register(r'', IngredientListViewSet, basename='ingredient')

router_tag = routers.DefaultRouter()
router_tag.register(r'', TagListViewSet, basename='tag')

router_recipe = routers.DefaultRouter()
router_recipe.register(r'', RecipeListCreateViewSet, basename='recipe')


urlpatterns = [
    path('ingredients/', include(router_ingredient.urls)),
    path('tags/', include(router_tag.urls)),
    path('recipes/', include(router_recipe.urls)),
]
