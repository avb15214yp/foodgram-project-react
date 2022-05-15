from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from api.mixins import ListViewSet
from foods.models import Ingredient
from foods.serializers import IngredientSerializer
from foods.filters import IngredientFilter


class IngredientListViewSet(ListViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
