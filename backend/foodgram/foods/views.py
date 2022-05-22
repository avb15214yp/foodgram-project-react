from django.http import JsonResponse
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.mixins import ListViewSet, ListCreateUpdateViewSet
from foods.models import Ingredient, Tag, Recipe
from foods.serializers import IngredientSerializer, TagSerializer
from foods.serializers import RecipeSerializer, RecipeSerializerForFavorite
from foods.filters import IngredientFilter, RecipeFilter
from foods.permissions import C_AuthUser_UD_Owner_R_Any_Permisson
from foods.shortcuts import get_object_or_response400


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

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        get_status, res = get_object_or_response400(Recipe, pk=pk)
        if not get_status:
            return res
        recipe = res
        user = request.user
        user_exists = user.recipe_faworites.filter(id=recipe.id).exists()
        if request.method == 'POST':
            if user_exists:
                error_msg = {'errors': 'Этот рецепт уже добавлен в избранные'}
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data=error_msg
                )

            recipe.user_faworites.add(user)
            data = RecipeSerializerForFavorite(instance=recipe).data
            return JsonResponse(data=data, status=status.HTTP_201_CREATED)

        if user_exists:
            recipe.user_faworites.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        error_msg = {'errors': 'Этого рецепта нет в избранных'}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_msg)
