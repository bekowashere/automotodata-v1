from django.contrib import admin
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
    ModelImages,
    CarSpecificationType,
    CarSpecification,
    Car,
    CarSpecificationValue  
)

from django.utils.translation import gettext_lazy as _

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Brand Information'), {'fields': ('brand_name', 'brand_slug', 'brand_image', 'brand_image_url')}),
        (_('Description'), {'fields': ('brand_description',)}),
        (_('URL'), {'fields': ('brand_detail_url',)})
    )
    list_display = ('brand_name', 'brand_slug')
    search_fields = ('brand_name', 'brand_slug')
    ordering = ('brand_name',)

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Series Information'), {'fields': ('series_brand', 'series_name', 'series_slug', 'series_image', 'series_image_url')}),
        (_('Specifications'), {'fields': ('series_bodyStyle', 'series_fuelType')}),
        (_('Discontinued'), {'fields': ('series_isDiscontinued',)}),
        (_('BOT Generation Count'), {'fields': ('series_generation_count_bot',)}),
        (_('URL'), {'fields': ('series_detail_url',)})
    )
    list_display = ('series_name', 'series_brand', 'series_slug')
    search_fields = ('series_name', 'series_brand__brand_name', 'series_slug')
    ordering = ('series_name',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Model Information'), {'fields': ('model_brand', 'model_series', 'model_name', 'model_slug')}),
        (_('Image Information'), {'fields': ('model_image', 'model_image_url', 'model_image_path')}),
        (_('Description'), {'fields': ('model_description',)}),
        (_('Year Information'), {'fields': ('model_start_year', 'model_end_year', 'model_years')}),
        (_('Specifications'), {'fields': ('model_fuelType', 'model_segment', 'model_bodyStyle', 'model_infotainment')}),
        (_('URL'), {'fields': ('model_detail_url',)}),
    )
    list_display = ('model_name', 'model_brand', 'model_series', 'model_slug')
    search_fields = ('model_name', 'model_brand__brand_name', 'model_series__series_name', 'model_slug')
    ordering = ('model_name',)

class CarSpecificationValueInline(admin.TabularInline):
    model = CarSpecificationValue

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Car Information'), {'fields': ('car_brand', 'car_series', 'car_model', 'car_name', 'car_slug')}),
        (_('Engine Specifications'), {'fields': ('car_fuelType', 'car_driveType', 'car_gearBox', 'car_engine', 'car_enginePower')}),
        (_('URL'), {'fields': ('car_detail_url', 'car_alt_url')}),
    )
    list_display = ('car_name', 'car_slug', 'car_model')
    search_fields = ('car_name', 'car_model__model_name', 'car_slug')
    ordering = ('car_model__model_name',)

    inlines = [
        CarSpecificationValueInline
    ]