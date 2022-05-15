from rest_framework import permissions

from api.mixins import ListViewSet
from foods.models import Ingredient
from foods.serializers import IngredientSerializer


class IngredientListViewSet(ListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
