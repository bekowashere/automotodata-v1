from django.core.management import BaseCommand, CommandError
from auto.models import Brand
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/auto/all_brands.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for brand in data:
            brand_name = brand['brand_name']
            brand_slug = brand['brand_slug']
            brand_description = brand['brand_description']
            brand_detail_url = brand['brand_detail_url']
            brand_image_url = brand['brand_image_url']
            brand_image_path = brand['brand_image_path']
            image = f'auto/brands_logo/{brand_image_path}'

            try:
                brand = Brand(
                    brand_name=brand_name,
                    brand_slug=brand_slug,
                    brand_image=image,
                    brand_image_url=brand_image_url,
                    brand_detail_url = brand_detail_url,
                    brand_description = brand_description
                )
                brand.save()

                self.stdout.write(self.style.SUCCESS(f'{brand_name} create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')