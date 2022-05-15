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
