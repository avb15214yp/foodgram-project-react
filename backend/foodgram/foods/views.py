from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.mixins import ListViewSet, ListAllViewSet, ListCreateDelViewSet
from foods.models import Ingredient, Tag, Recipe
from foods.serializers import IngredientSerializer, TagSerializer
from foods.serializers import RecipeSerializer, RecipeSerializerForFavorite
from foods.serializers import SubscriptionSerializer
from foods.filters import IngredientFilter, RecipeFilter
from foods.permissions import C_AuthUser_UD_Owner_R_Any_Permisson
from foods.permissions import C_AuthUser_DL_Owner_Permisson

from foods.shortcuts import get_object_or_response400
from users.models import Follow


User = get_user_model()


class IngredientViewSet(ListViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ListViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ListAllViewSet):
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
            context = {'context': {'request': request}}
            data = RecipeSerializerForFavorite(instance=recipe, **context).data
            return JsonResponse(data=data, status=status.HTTP_201_CREATED)

        if user_exists:
            recipe.user_faworites.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        error_msg = {'errors': 'Этого рецепта нет в избранных'}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_msg)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        get_status, res = get_object_or_response400(Recipe, pk=pk)
        if not get_status:
            return res
        recipe = res
        user = request.user
        recipe_shopping_exists = user.recipe_shopping.filter(id=recipe.id).exists()
        if request.method == 'POST':
            if recipe_shopping_exists:
                error_msg = {'errors': 'Этот рецепт уже добавлен в покупки'}
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, data=error_msg
                )

            recipe.shopping_cart.add(user)
            context = {'context': {'request': request}}
            data = RecipeSerializerForFavorite(instance=recipe, **context).data
            return JsonResponse(data=data, status=status.HTTP_201_CREATED)

        if recipe_shopping_exists:
            recipe.shopping_cart.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        error_msg = {'errors': 'Этого рецепта нет в списке покупок'}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_msg)

    @action(methods=['get',], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = {}
        for recipe in user.recipe_shopping.all():
            for recipe_ingredietn in recipe.recipe_ingredient.all():
                ingredient = recipe_ingredietn.ingredient
                amount = recipe_ingredietn.amount
                if ingredient in shopping_list:
                    shopping_list[ingredient] += amount
                else:
                    shopping_list[ingredient] = amount
        
        shopping = 'Список покупок' + '\n'
        for key, value in shopping_list.items():
            shopping = shopping + str(key) + ' ' + str(value) + str(key.measurement_unit) +  '\n'


        filename = "shopping_list.txt"
        content = shopping
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
        # return Response(status=status.HTTP_400_BAD_REQUEST, data=shopping_list)





class SubscriptionViewSet(ListCreateDelViewSet):
    permission_classes = (C_AuthUser_DL_Owner_Permisson,)
    # queryset = Follow.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def create(self, request, id):

        following_id = id
        user = request.user
        if user.id == following_id:
            error_msg = {'errors': 'Нельзя подписываться на самого себя'}
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=error_msg
            )

        following_exists = user.follower.filter(
            following__id=following_id
        ).exists()
        if following_exists:
            error_msg = {'errors': 'Уже есть подписка на этого автора'}
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=error_msg
            )

        following = get_object_or_404(User, pk=following_id)
        follow = Follow.objects.create(user=user, following=following)
        context = {'context': {'request': request}}
        data = SubscriptionSerializer(instance=follow, **context).data
        return JsonResponse(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        following_id = id
        user = request.user
        if user.id == following_id:
            error_msg = {'errors': 'Нельзя отписаться от самого себя'}
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=error_msg
            )
        following = get_object_or_404(User, pk=following_id)

        follow = user.follower.filter(following=following)
        if not follow.exists():
            error_msg = {'errors': 'Нет подписки на этого автора'}
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=error_msg
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
