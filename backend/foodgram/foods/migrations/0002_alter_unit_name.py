# Generated by Django 4.0.4 on 2022-05-15 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='name'),
        ),
    ]