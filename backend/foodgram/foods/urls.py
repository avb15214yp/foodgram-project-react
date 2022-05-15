from django.urls import include, path
from rest_framework import routers

from foods.views import IngredientListViewSet

router = routers.DefaultRouter()
router.register(r'', IngredientListViewSet, basename='ingredient')

urlpatterns = [
    path('ingredients/', include(router.urls)),
]
