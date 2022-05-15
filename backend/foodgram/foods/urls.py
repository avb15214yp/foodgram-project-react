from django.urls import include, path
from rest_framework import routers

from foods.views import IngredientListViewSet, TagListViewSet

router_ingredient = routers.DefaultRouter()
router_ingredient.register(r'', IngredientListViewSet, basename='ingredient')

router_tag = routers.DefaultRouter()
router_tag.register(r'', TagListViewSet, basename='tag')


urlpatterns = [
    path('ingredients/', include(router_ingredient.urls)),
    path('tags/', include(router_tag.urls)),
]
