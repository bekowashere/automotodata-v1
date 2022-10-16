from django.core.management import BaseCommand, CommandError
from auto.models import CarSpecificationType
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/auto/all_specification_types.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        specification_types = []
        for specification_type in data:
            spc_type = specification_type["name"]

            if not spc_type in specification_types:
                specification_types.append(spc_type)
        
        for specification_type in specification_types:
            try:
                CarSpecificationType.objects.create(
                    name=specification_type
                )
                self.stdout.write(self.style.SUCCESS(f'{specification_type} create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')