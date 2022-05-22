from django.contrib import admin

from foods.models import Ingredient, Unit
from foods.models import Tag, Recipe
from foods.models import RecipeIngredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    search_fields = ('author', 'name')
    list_filter = ('tags',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
