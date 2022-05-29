from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from foods.fields import ImageFieldSerializer
from foods.models import Ingredient, Recipe, RecipeIngredient, Tag, Unit
from foods.validators import validate_array_duplicates
from users.models import Follow
from users.serializers import UserSerializerList

User = get_user_model()


class BaseModelSerializer(serializers.ModelSerializer):

    def get_user(self):
        request = self.context.get('request')
        if request:
            return request.user
        return None

    def get_authenticated_user(self):
        user = self.get_user()
        if bool(user and user.is_authenticated):
            return user
        else:
            return None


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient', read_only=True)
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']
        read_only_fields = ['name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['name', 'color', 'slug']

    def to_internal_value(self, data):
        return {'id': data}


class RecipeSerializerForFavorite(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image', 'cooking_time'
        ]


class RecipeShortSerializer(BaseModelSerializer):
    image = ImageFieldSerializer(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(BaseModelSerializer):
    tags = TagSerializer(many=True,)
    author = UserSerializerList(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredient',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = ImageFieldSerializer(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text',
            'cooking_time'
        ]

    def validate_tags(self, value):
        value = validate_array_duplicates(
            value, 'Переданы повторяющиеся теги')
        for i in range(len(value)):
            pk = value[i]['id']
            try:
                tag = Tag.objects.get(pk=pk)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(f'Не найден Тэг с id={pk}')
            value[i] = tag
        return value

    def validate_ingredients(self, value):
        value = validate_array_duplicates(
            value, 'Переданы повторяющиеся ингредиенты')
        for i in range(len(value)):
            pk = value[i]['ingredient']['id']
            try:
                ingredient = Ingredient.objects.get(pk=pk)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Не найден ингредиент с id={pk}'
                )
            value[i]['ingredient'] = ingredient
        return value

    def get_is_favorited(self, obj):
        user = self.get_authenticated_user()
        if user:
            return obj.user_favorites.filter(id=user.id).exists()
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        user = self.get_authenticated_user()
        if user:
            return obj.shopping_cart.filter(id=user.id).exists()
        else:
            return False

    def recipe_add_tags(self, recipe, tags):
        for tag in tags:
            recipe.tags.add(tag)

    def recipe_add_ingredients(self, recipe, recipe_ingredients):
        for recipe_ingredient in recipe_ingredients:
            recipe.recipe_ingredient.create(
                ingredient=recipe_ingredient['ingredient'],
                amount=recipe_ingredient['amount']
            )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe_ingredients = validated_data.pop('recipe_ingredient')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.recipe_add_tags(recipe, tags)
        self.recipe_add_ingredients(recipe, recipe_ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        recipe_ingredients = validated_data.pop('recipe_ingredient')
        instance.tags.clear()
        self.recipe_add_tags(instance, tags)
        instance.ingredients.clear()
        self.recipe_add_ingredients(instance, recipe_ingredients)

        super().update(instance, validated_data)
        return instance


class SubscriptionSerializer(BaseModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='following', write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['following', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('following', 'user'),
                message='Уже существует подписка на этого автора'
            )
        ]

    def to_representation(self, value):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        context = {'context': self.context}
        ret = UserSerializerList(
            value.following, **context
        ).data
        author_id = ret['id']
        if recipes_limit:
            recipe_set = Recipe.objects.filter(
                author__id=author_id
            )[:int(recipes_limit)]
        else:
            recipe_set = Recipe.objects.filter(author__id=author_id)
        recipes = RecipeShortSerializer(
            recipe_set, many=True, **context
        ).data
        ret.update({'recipes': recipes})
        ret.update({'recipes_count': len(recipes)})
        return ret

    def validate(self, data):
        super().validate(data)
        user = data.get('user')
        following = data.get('following')
        action = self.context.get('action')
        if action == 'create':
            if user == following:
                raise serializers.ValidationError(
                    'Нельзя подписываться на самого себя'
                )
        elif action == 'delete':
            if user == following:
                raise serializers.ValidationError(
                    'Нельзя отписаться от себя'
                )
            follow = user.follower.filter(following=following)
            if not follow.exists():
                raise serializers.ValidationError(
                    'Нет подписки на этого автора'
                )
            follow = user.follower.filter(following=following)
            if not follow.exists():
                raise serializers.ValidationError(
                    'Нет подписки на этого автора'
                )
            data = follow
        return data


class SubscriptionDeleteSerializer(SubscriptionSerializer):

    class Meta(SubscriptionSerializer.Meta):
        validators = []
