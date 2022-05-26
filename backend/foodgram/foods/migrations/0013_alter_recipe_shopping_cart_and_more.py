# Generated by Django 4.0.4 on 2022-05-24 18:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foods', '0012_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='recipe_shopping', to=settings.AUTH_USER_MODEL, verbose_name='в карте покупок у пользователей'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='user_faworites',
            field=models.ManyToManyField(blank=True, related_name='recipe_faworites', to=settings.AUTH_USER_MODEL, verbose_name='фаворит у пользователей'),
        ),
    ]
