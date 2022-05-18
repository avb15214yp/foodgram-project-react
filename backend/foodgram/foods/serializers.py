from rest_framework import serializers

from foods.models import Ingredient, Unit, Tag, Recipe
from users.serializers import UserSerializerList


class BaseHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):

    def get_user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_authenticated_user(self):
        user = self.get_user()
        if bool(user and user.is_authenticated):
            return user
        else:
            return None


class UnitSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Unit
        fields = ['id', 'name']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    measurement_unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeIngredientSerializer(IngredientSerializer):
    amount = serializers.IntegerField(source='ingredients_amount')

    class Meta:
        model = Recipe


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeSerializer(BaseHyperlinkedModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializerList()
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text',
            'cooking_time'
        ]

    def get_is_favorited(self, obj):
        user = self.get_authenticated_user()
        if user:
            return obj.user_faworites.filter(id=user.id).exists()
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        user = self.get_authenticated_user()
        if user:
            return obj.shopping_cart.filter(id=user.id).exists()
        else:
            return False
