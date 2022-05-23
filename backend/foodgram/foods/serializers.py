from django.db import transaction
from rest_framework import serializers

from foods.models import Ingredient, Unit, Tag, Recipe, RecipeIngredient
from users.models import Follow
from users.serializers import UserSerializerList


class BaseModelSerializer(serializers.ModelSerializer):

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


class ImageFieldSerializer(serializers.ImageField):

    def to_representation(self, value):
        return self.context['request'].build_absolute_uri(value.url)

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(ImageFieldSerializer, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class RecipeSerializerForFavorite(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image', 'cooking_time'
        ]


class RecipeSerializer(BaseModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializerList(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredient'
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

    def recipe_add_tags(self, recipe, tags):
        for tag_id in tags:
            try:
                pk = tag_id['id']
                tag = Tag.objects.get(pk=pk)
            except Exception:
                raise serializers.ValidationError(f'Не найден Тэг с id={pk}')
            recipe.tags.add(tag)

    def recipe_add_ingredients(self, recipe, recipe_ingredients):
        for recipe_ingredient in recipe_ingredients:
            pk = recipe_ingredient['ingredient']['id']
            try:
                ingredient = Ingredient.objects.get(pk=pk)
            except Exception:
                raise serializers.ValidationError(
                    f'Не найден ингредиент с id={pk}'
                )

            recipe.recipe_ingredient.create(
                ingredient=ingredient, amount=recipe_ingredient['amount']
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

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(source='user.email')
    # id = serializers.IntegerField(source='user.')
    # username = serializers.(source='user.')
    # first_name = serializers.(source='user.')
    # last_name = serializers.(source='user.')
    # = serializers.(source='user.')
    user = UserSerializerList(read_only=True)

    class Meta:
        model = Follow
        fields = ['user', ]# ['email', 'user', 'following']
