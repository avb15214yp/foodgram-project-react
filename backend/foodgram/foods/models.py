from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Unit(models.Model):
    name = models.CharField(
        _('name'), max_length=200,
        blank=False, null=False, unique=True
        )

    class Meta:
        ordering = ['name', ]
        verbose_name = 'ед. изм'
        verbose_name_plural = 'ед. изм'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        _('name'), max_length=200,
        blank=False, null=False, unique=True
    )
    measurement_unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name='ед. изм'
    )

    class Meta:
        ordering = ['name', ]
        verbose_name = _('ингредиент')
        verbose_name_plural = _('ингредиенты')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        _('name'), max_length=200,
        blank=False, null=False, unique=True
    )
    color = models.CharField(
        _("цвет"), max_length=7,
        blank=True, null=True
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    class Meta:
        ordering = ['name', ]
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты',
    )

    tags = models.ManyToManyField(Tag, verbose_name='Тэг')

    user_faworites = models.ManyToManyField(
        User, related_name='recipe_faworites',
        verbose_name='фаворит у пользователей',
    )

    shopping_cart = models.ManyToManyField(
        User, related_name='recipe_shopping',
        verbose_name='в карте покупок у пользователей',
    )

    image = models.FileField(
        _('Картинка'), upload_to='recipes/',
        blank=False
        )

    name = models.CharField(
        _('name'), max_length=200,
        blank=False, null=False, unique=True
    )

    text = models.TextField(
        _('Описание'),
        blank=False, null=False,
    )

    cooking_time = models.IntegerField(
        _('Время приготовления (в минутах)'),
        validators=[MinValueValidator(1)],
        blank=False, null=False
    )

    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        blank=False, null=False,
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
        blank=False, null=False
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        blank=False, null=False
    )
    amount = models.IntegerField(
        _('Количество'), validators=[MinValueValidator(1)],
        blank=False, null=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]
