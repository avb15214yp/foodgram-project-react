from django.contrib import admin

from foods.models import Ingredient, Recipe, RecipeIngredient, Tag, Unit


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'user_faworites_count')
    search_fields = ('author__username', 'name')
    list_filter = ('tags',)

    def user_faworites_count(self, obj):
        return obj.user_faworites.count()


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
