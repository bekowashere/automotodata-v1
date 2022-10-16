from django.core.management import BaseCommand, CommandError
from auto.models import (
    Brand,
    Series,
    Model,
    Car,
    CarSpecification,
    CarSpecificationType,
    CarSpecificationValue,
    DriveType,
    GearBox
)
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/auto/all_cars.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for _car in data:
            brand_name = _car['brand_name']
            brand_detail_url = _car['brand_detail_url']
            brand_slug = _car['brand_slug']
            
            series_name = _car['series_name']
            series_detail_url = _car['series_detail_url']
            series_slug = _car['series_slug']

            model_name = _car['model_name']
            model_detail_url = _car['model_detail_url']
            model_slug = _car['model_slug']

            car_name = _car['car_name']
            car_detail_url = _car['car_detail_url']
            car_slug = _car['car_slug']
            car_alt_url = _car['car_alt_url']

            car_fuelType = _car['car_fuelType']
            _car_driveType = _car['car_driveType']
            _car_gearBox = _car['car_gearBox']
            car_engine = _car['car_engine']
            car_enginePower = _car['car_enginePower']

            car_information = _car['car_information']

            # brand_detail_url is UNIQUE
            brand = Brand.objects.get(brand_detail_url=brand_detail_url)
            # series_detail_url is UNIQUE
            series = Series.objects.get(series_detail_url=series_detail_url)
            # model_detail_url is UNIQUE
            model = Model.objects.get(model_detail_url=model_detail_url)

            # DRIVE TYPE
            if _car_driveType is not None:
                try:
                    car_driveType = DriveType.objects.get(name=_car_driveType)
                except:
                    car_driveType = DriveType(name=_car_driveType)
                    car_driveType.save()

            # GEARBOX
            if _car_gearBox is not None:
                try:
                    car_gearBox = GearBox.objects.get(name=_car_gearBox)
                except:
                    car_gearBox = GearBox(name=_car_gearBox)
                    car_gearBox.save()

            try:
                car = Car(
                    car_brand=brand,
                    car_series=series,
                    car_model=model,
                    car_name=car_name,
                    car_slug=car_slug,
                    car_fuelType=car_fuelType,
                    car_driveType=car_driveType,
                    car_gearBox=car_gearBox,
                    car_engine=car_engine,
                    car_enginePower=car_enginePower,
                    car_detail_url=car_detail_url,
                    car_alt_url=car_alt_url
                )

                car.save()
                self.stdout.write(self.style.SUCCESS(f'{car_name} create successfully'))

                # SPECIFICATIONS PART
                # k -> car specification type       ["General Specs"]
                # v -> {}                           ["Cylinders":"L6", "Displacement":"2993 m3", ..]
                # x -> car specification            ["Cylinders"]
                # y -> value                        ["L6"]
                for k, v in car_information.items():
                    car_specification_type = CarSpecificationType.objects.get(name=k)
                    for x,y in v.items():
                        car_specification = CarSpecification.objects.get(cs_type=car_specification_type, name=x)
                        CarSpecificationValue.objects.create(
                            car=car,
                            specification=car_specification,
                            value=y
                        )
                # self.stdout.write(self.style.SUCCESS(f'Specifications added successfully'))
            except Exception as e:
                raise CommandError(f'{e}')