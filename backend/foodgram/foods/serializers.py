from rest_framework import serializers

from foods.models import Ingredient, Unit, Tag, Recipe, RecipeIngredient
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
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount', ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class ImageFieldSerializer(serializers.ImageField):

    def to_representation(self, value):
        return value

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


class RecipeSerializer(BaseModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializerList(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredient',
        read_only=True
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        print(tags)
