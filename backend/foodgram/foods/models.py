from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(
        'Имя', max_length=200,
        unique=True
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'ед. изм'
        verbose_name_plural = 'ед. изм'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Имя', max_length=200,
        unique=True
    )
    measurement_unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT,
        verbose_name='ед. изм'
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Имя', max_length=200,
        unique=True
    )
    color = models.CharField(
        "Имя", max_length=7,
        blank=True, null=True
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name', ]
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )

    tags = models.ManyToManyField(Tag, verbose_name='Тэг')

    user_favorites = models.ManyToManyField(
        User, related_name='recipe_favorites',
        verbose_name='фаворит у пользователей',
        blank=True
    )

    shopping_cart = models.ManyToManyField(
        User, related_name='recipe_shopping',
        verbose_name='в карте покупок у пользователей',
        blank=True
    )

    image = models.ImageField('Картинка', upload_to='recipes/')

    name = models.CharField(
        'Имя', max_length=200,
        unique=True
    )

    text = models.TextField(
        'Описание',
    )

    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
    )

    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name='Автор', related_name='recipe_author'
    )

    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', auto_now=True)

    class Meta:
        ordering = ['-updated', ]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        'Количество', validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
