from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from foods.filters import IngredientFilter, RecipeFilter
from foods.mixins import ListAllViewSet, ListCreateDelViewSet, ListViewSet
from foods.models import Ingredient, Recipe, RecipeIngredient, Tag
from foods.permissions import (CAuthUserDLOwnerPermisson,
                               CAuthUserUDOwnerRAnyPermisson)
from foods.serializers import (IngredientSerializer, RecipeSerializer,
                               RecipeSerializerForFavorite,
                               SubscriptionDeleteSerializer,
                               SubscriptionSerializer, TagSerializer)
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
    permission_classes = (CAuthUserUDOwnerRAnyPermisson,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def _m2m_get_post_delete(
        self, request,
        m2m, pk=None,
        error_msg_exists='',
        error_msg_not_exists=''
    ):

        get_status, res = get_object_or_response400(Recipe, pk=pk)
        if not get_status:
            return res
        recipe = res
        m2m_exists = m2m.filter(id=recipe.id).exists()
        if request.method == 'POST':
            if m2m_exists:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': error_msg_exists}
                )

            m2m.add(recipe)
            context = {'context': {'request': request}}
            data = RecipeSerializerForFavorite(instance=recipe, **context).data
            return Response(data=data, status=status.HTTP_201_CREATED)

        if m2m_exists:
            m2m.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'errors': error_msg_not_exists}
        )

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        user = request.user
        m2m = user.recipe_favorites
        return self._m2m_get_post_delete(
            request, m2m, pk=pk,
            error_msg_exists='Этот рецепт уже добавлен в избранные',
            error_msg_not_exists='Этого рецепта нет в избранных'
        )

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        m2m = user.recipe_shopping
        return self._m2m_get_post_delete(
            request, m2m, pk=pk,
            error_msg_exists='Этот рецепт уже добавлен в покупки',
            error_msg_not_exists='Этого рецепта нет в списке покупок'
        )

    @action(methods=['get', ], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        shopping = 'Список покупок' + '\n'
        for cur_record in RecipeIngredient.objects.filter(
            recipe__shopping_cart=user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit__name',
        ).annotate(Sum('amount')):
            shopping = (
                shopping + str(cur_record[0]) + ' '
                + str(cur_record[1]) + str(cur_record[2]) + '\n'
            )

        filename = "shopping_list.txt"
        content = shopping
        response = HttpResponse(content, content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename={0}'.format(filename)
        return response


class SubscriptionViewSet(ListCreateDelViewSet):
    permission_classes = (CAuthUserDLOwnerPermisson,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def create(self, request, id):
        res, is_valid = self._get_validated_data(request, id)
        if not is_valid:
            return res
        validated_data = res
        context = {'context': {'request': request, 'action': self.action}}
        follow = Follow.objects.create(**validated_data)
        data = SubscriptionSerializer(instance=follow, **context).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        res, is_valid = self._get_validated_data(request, id)
        if not is_valid:
            return res
        follow = res
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_validated_data(self, request, id):
        user = request.user
        context = {'context': {'request': request, 'action': self.action}}
        if self.action == 'delete':
            serializer = SubscriptionDeleteSerializer
        else:
            serializer = SubscriptionSerializer

        serializer = serializer(
            data={'id': id, 'user': user.id}, **context
        )

        if not serializer.is_valid():
            errors = list()
            for err_det in serializer.errors.values():
                for err in err_det:
                    errors.append(err.title())

            return (
                Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'errors': errors, }
                ),
                False
            )
        return (serializer.validated_data, True)
