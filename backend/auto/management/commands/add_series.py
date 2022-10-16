from django.core.management import BaseCommand, CommandError
from auto.models import Brand, Series, BodyStyle, FuelType
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/auto/all_series.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for _series in data:
            brand_name = _series['brand_name']
            brand_detail_url = _series['brand_detail_url']
            # brand_slug = _series['brand_slug']
            
            series_name = _series['series_name']
            series_detail_url = _series['series_detail_url']
            series_slug = _series['series_slug']

            series_image_url = _series['series_image_url']
            series_image_path = _series['series_image_path']
            
            _series_bodyStyle = _series['series_bodyStyle']
            series_isDiscontinued = _series['series_isDiscontinued']
            series_generation_count_bot = _series['series_generation_count']

            image = f'auto/{brand_name}/{series_name}/{series_image_path}'

            # brand_detail_url is UNIQUE
            brand = Brand.objects.get(brand_detail_url=brand_detail_url)

            if _series_bodyStyle is not None:
                try:
                    series_bodyStyle = BodyStyle.objects.get(style=_series_bodyStyle)
                except BodyStyle.DoesNotExist:
                    series_bodyStyle = BodyStyle(style=_series_bodyStyle)
                    series_bodyStyle.save()

            try:
                series = Series(
                    series_brand=brand,
                    series_name=series_name,
                    series_slug=series_slug,
                    series_image=image,
                    series_image_url=series_image_url,
                    series_bodyStyle=series_bodyStyle,
                    series_isDiscontinued=series_isDiscontinued,
                    series_generation_count_bot=series_generation_count_bot,
                    series_detail_url=series_detail_url
                )

                series.save()

                # series_fuelType
                fuelTypes = _series['series_fuelType']
                if len(fuelTypes) > 0:
                    for fuel in fuelTypes:
                        try:
                            fueltype = FuelType.objects.get(type=fuel)
                        except FuelType.DoesNotExist:
                            fueltype = FuelType(type=fuel)
                            fueltype.save()
                        series.series_fuelType.add(fueltype)

                series.save()

                self.stdout.write(self.style.SUCCESS(f'{series_name} create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')


            