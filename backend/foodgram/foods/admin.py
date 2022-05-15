from django.contrib import admin

from foods.models import Ingredient, Unit


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')


admin.site.register(Unit)
admin.site.register(Ingredient, IngredientAdmin)
