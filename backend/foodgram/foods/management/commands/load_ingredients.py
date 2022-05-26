import csv

from django.core.management.base import BaseCommand

from foods.models import Ingredient, Unit


class Command(BaseCommand):
    help = 'Загрузка справочника ингредиентов из csv файла (ingredients.csv)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str,
            help=u'Имя файла для загрузки'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']
        print(file_name)
        with open(file_name, encoding='UTF8') as f:
            reader = csv.reader(f)
            for row in reader:
                unit_name = row[1]
                unit, status = Unit.objects.get_or_create(name=unit_name)
                ingredient = Ingredient.objects.filter(name=row[0])
                if not ingredient:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=unit
                    )
        print('Справочник загружен')
