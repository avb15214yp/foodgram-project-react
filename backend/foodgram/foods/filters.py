from django_filters import rest_framework as filters

from foods.models import Ingredient, Recipe, Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug', to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='is_favorited_filtr')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filtr'
    )

    class Meta:
        model = Recipe
        fields = ['author', ]

    def is_favorited_filtr(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(
                    **{'user_faworites__id': user.id, }
                )
            else:
                return queryset.exclude(
                    **{'user_faworites__id': user.id, }
                )
        return queryset

    def is_in_shopping_cart_filtr(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value:
                return queryset.filter(
                    **{'shopping_cart__id': user.id, }
                )
            else:
                return queryset.exclude(
                    **{'shopping_cart__id': user.id, }
                )
        return queryset
