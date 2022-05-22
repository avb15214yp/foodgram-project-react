from rest_framework import permissions
from rest_framework.decorators import action
from django.core.exceptions import BadRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response

from api.mixins import ListViewSet, ListCreateUpdateViewSet
from foods.models import Ingredient, Tag, Recipe
from foods.serializers import IngredientSerializer, TagSerializer
from foods.serializers import RecipeSerializer
from foods.filters import IngredientFilter, RecipeFilter
from foods.permissions import C_AuthUser_UD_Owner_R_Any_Permisson


class IngredientListViewSet(ListViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagListViewSet(ListViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeListCreateViewSet(ListCreateUpdateViewSet):
    permission_classes = (C_AuthUser_UD_Owner_R_Any_Permisson,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_204_NO_CONTENT, data='dssss')
            # raise BadRequest(f'Не найден рецепт с id={pk}')

        recipe.user_faworites.add(recipe)
        return recipe
