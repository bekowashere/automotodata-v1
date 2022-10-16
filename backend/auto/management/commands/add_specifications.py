from django.core.management import BaseCommand, CommandError
from auto.models import CarSpecification, CarSpecificationType
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/auto/all_specifications.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for specification in data:
            cs_type = specification['cs_type']
            name = specification['name']

            if not CarSpecification.objects.filter(cs_type__name=cs_type, name=name).exists():
                try:
                    car_specification_type = CarSpecificationType.objects.get(name=cs_type)

                    CarSpecification.objects.create(
                        cs_type=car_specification_type,
                        name=name
                    )
                    self.stdout.write(self.style.SUCCESS(f'{name} Specification created'))
                except Exception as e:
                    raise CommandError(f'{e}')