from rest_framework import serializers
from auto.models import (
    FuelType,
    DriveType,
    GearBox,
    Infotainment,
    BodyStyle,
    Segment,
    Brand,
    Series,
    Model,
    ModelYear,
    ModelImages,
    CarSpecificationType,
    CarSpecification,
    Car,
    CarSpecificationValue  
)

# ! HELPER SERIALIZERS
class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ('id', 'type')

class InfotainmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infotainment
        fields = ('id', 'name', 'icon')

class ModelYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelYear
        fields = ('year',)

# ! SUMMARY SERIALIZER
class SummaryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'brand_name', 'brand_slug', 'brand_image')

class SummarySeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('id', 'series_name', 'series_slug', 'series_image')

class SummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'model_name', 'model_slug', 'model_image')

# ! /auto : BrandListSerializer
class BrandListSerializer(serializers.ModelSerializer):
    brand_total_series_count = serializers.SerializerMethodField()
    brand_in_production_count = serializers.SerializerMethodField()
    brand_discontinued_count = serializers.SerializerMethodField()
    brand_url = serializers.HyperlinkedIdentityField(
        view_name='auto:brand_detail',
        lookup_field='brand_slug'
    )
    def get_brand_total_series_count(self, obj):
        return obj.get_total_series_count()
    
    def get_brand_in_production_count(self, obj):
        return obj.get_continued_count()

    def get_brand_discontinued_count(self, obj):
        return obj.get_discontinued_count()

    class Meta:
        model = Brand
        fields = (
            'id',
            'brand_name',
            'brand_slug',
            'brand_url',
            'brand_image',
            'brand_image_url',
            'brand_total_series_count',
            'brand_in_production_count',
            'brand_discontinued_count'
        )


# ! /auto/<brand_slug> : BrandDetailSerializer
# /auto/bmw
# SeriesListSerializer (for BrandDetailSerializer)
class SeriesListSerializer(serializers.ModelSerializer):
    series_bodyStyle = serializers.SerializerMethodField()
    series_fuelType = FuelTypeSerializer(many=True)
    series_generation_count = serializers.SerializerMethodField()
    series_generation_oldest_year = serializers.SerializerMethodField()
    series_generation_newest_year = serializers.SerializerMethodField()

    def get_series_bodyStyle(self, obj):
        return obj.series_bodyStyle.style

    def get_series_generation_count(self, obj):
        return obj.get_models_count()

    def get_series_generation_oldest_year(self, obj):
        return obj.get_first_year()

    def get_series_generation_newest_year(self, obj):
        return obj.get_last_year()

    class Meta:
        model = Series
        fields = (
            'id',
            'series_name',
            'series_slug',
            'series_image',
            'series_image_url',
            'series_bodyStyle',
            'series_fuelType',
            'series_isDiscontinued',
            'series_generation_count',
            'series_generation_oldest_year',
            'series_generation_newest_year',
        )

class BrandDetailSerializer(serializers.ModelSerializer):
    brand_total_series_count = serializers.SerializerMethodField()
    brand_in_production_count = serializers.SerializerMethodField()
    brand_discontinued_count = serializers.SerializerMethodField()

    brand_continued_series = serializers.SerializerMethodField()
    brand_discontinued_series = serializers.SerializerMethodField()

    def get_brand_total_series_count(self, obj):
        return obj.get_total_series_count()
    
    def get_brand_in_production_count(self, obj):
        return obj.get_continued_count()

    def get_brand_discontinued_count(self, obj):
        return obj.get_discontinued_count()

    def get_brand_continued_series(self, obj):
        return SeriesListSerializer(obj.get_continued_series, many=True).data

    def get_brand_discontinued_series(self, obj):
        return SeriesListSerializer(obj.get_discontinued_series, many=True).data

    class Meta:
        model = Brand
        fields = (
            'id',
            'brand_name',
            'brand_slug',
            'brand_image',
            'brand_image_url',

            # function
            'brand_total_series_count',
            'brand_in_production_count',
            'brand_discontinued_count',

            # @property
            'brand_continued_series',
            'brand_discontinued_series',

            'brand_description'
        )

# ! /auto/<brand_slug>/<series_slug> : SeriesDetailSerializer
# /auto/bmw/x1
# CarListSerializer (for ModelListSerializer)
class CarListSerializer(serializers.ModelSerializer):
    car_brand_name = serializers.SerializerMethodField()
    car_series_name = serializers.SerializerMethodField()
    car_model_name = serializers.SerializerMethodField()

    def get_car_brand_name(self, obj):
        return obj.car_brand.brand_name

    def get_car_series_name(self, obj):
        return obj.car_series.series_name

    def get_car_model_name(self, obj):
        return obj.car_model.model_name

    class Meta:
        model = Car
        fields = (
            'id',
            'car_brand_name',
            'car_series_name',
            'car_model_name',
            'car_name',
            'car_slug',
            'car_fuelType',
            'car_driveType',
            'car_gearBox',
            'car_engine',
            'car_enginePower'
        )

# ModelListSerializer (for SeriesDetailSerializer)
class ModelListSerializer(serializers.ModelSerializer):
    model_fuelType = FuelTypeSerializer(many=True)
    model_cars = serializers.SerializerMethodField()

    def get_model_cars(self, obj):
        return CarListSerializer(obj.get_all_cars, many=True).data

    class Meta:
        model = Model
        fields = (
            'id',
            'model_name',
            'model_slug',
            'model_image',
            'model_image_url',
            'model_start_year',
            'model_end_year',
            'model_fuelType',
            'model_description',
            'model_cars'
        )


class SeriesDetailSerializer(serializers.ModelSerializer):
    series_brand = SummaryBrandSerializer()
    series_fuelType = FuelTypeSerializer(many=True)

    series_first_production_year = serializers.SerializerMethodField()
    series_bodyStyle = serializers.SerializerMethodField()
    series_generation_count = serializers.SerializerMethodField()
    series_generation_oldest_year = serializers.SerializerMethodField()
    series_generation_newest_year = serializers.SerializerMethodField()

    series_models = serializers.SerializerMethodField()

    def get_series_first_production_year(self, obj):
        return obj.get_first_year()

    def get_series_bodyStyle(self, obj):
        return obj.series_bodyStyle.style

    def get_series_generation_count(self, obj):
        return obj.get_models_count()

    def get_series_generation_oldest_year(self, obj):
        return obj.get_first_year()

    def get_series_generation_newest_year(self, obj):
        return obj.get_last_year()

    def get_series_models(self, obj):
        return ModelListSerializer(obj.get_all_models, many=True).data

    class Meta:
        model = Series
        fields = (
        'id',
        'series_brand',
        'series_name',
        'series_slug',
        'series_image',
        'series_image_url',
        'series_first_production_year',
        'series_bodyStyle',
        'series_fuelType',
        'series_isDiscontinued',
        'series_generation_count',
        'series_generation_oldest_year',
        'series_generation_newest_year',
        'series_models'
        )

# ! /auto/<brand_slug>/<series_slug>/<model_slug> : ModelDetailSerializer
# /auto/bmw/x1/bmw-x1-2022
# ModelImagesListSerializer (for ModelDetailSerializer)
class ModelImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelImages
        fields = ('id', 'image_url', 'alt_text')

class ModelDetailSerializer(serializers.ModelSerializer):
    model_brand = SummaryBrandSerializer()
    model_series = SummarySeriesSerializer()
    model_fuelType = FuelTypeSerializer(many=True)
    model_infotainment = InfotainmentSerializer(many=True)
    model_years = ModelYearSerializer(many=True)
    model_segment = serializers.SerializerMethodField()
    model_cars = serializers.SerializerMethodField()
    model_images = serializers.SerializerMethodField()

    def get_model_segment(self, obj):
        return obj.model_segment.name

    def get_model_cars(self, obj):
        return CarListSerializer(obj.get_all_cars, many=True).data

    def get_model_images(self, obj):
        return ModelImagesListSerializer(obj.get_all_model_images, many=True).data

    class Meta:
        model = Model
        fields = (
            'id',
            'model_brand',
            'model_series',
            'model_name',
            'model_slug',
            'model_image',
            'model_image_url',
            'model_image_path',
            'model_start_year',
            'model_end_year',
            'model_years',
            'model_fuelType',
            'model_segment',
            'model_bodyStyle',
            'model_infotainment',
            'model_description',
            'model_images',
            'model_cars',
        )

# ! /cars/<car_slug> : CarDetailSerializer
# CarSpecificationValueSerializer (for CarDetailSerializer)
class CarSpecificationValueSerializer(serializers.ModelSerializer):
    specification_type = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()

    def get_specification_type(self, obj):
        return obj.specification.cs_type.name

    def get_specification(self, obj):
        return obj.specification.name

    class Meta:
        model = CarSpecificationValue
        fields = ('specification_type', 'specification', 'value')

class CarDetailSerializer(serializers.ModelSerializer):
    car_brand = SummaryBrandSerializer()
    car_series = SummarySeriesSerializer()
    car_model = SummaryModelSerializer()
    car_specifications = serializers.SerializerMethodField()
    car_driveType = serializers.SerializerMethodField()
    car_gearBox = serializers.SerializerMethodField()

    def get_car_specifications(self, obj):
        return CarSpecificationValueSerializer(obj.get_all_specifications, many=True).data

    def get_car_driveType(self, obj):
        return obj.car_driveType.name

    def get_car_gearBox(self, obj):
        return obj.car_gearBox.name

    class Meta:
        model = Car
        fields = (
            'id',
            'car_brand',
            'car_series',
            'car_model',
            'car_name',
            'car_slug',
            'car_fuelType',
            'car_driveType',
            'car_gearBox',
            'car_engine',
            'car_enginePower',
            'car_specifications'
        )