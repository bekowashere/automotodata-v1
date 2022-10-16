from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

# HELPER MODELS
class FuelType(models.Model):
    type = models.CharField(_('Fuel Type'), max_length=64)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('Fuel Type')
        verbose_name_plural = _('Fuel Types')

class DriveType(models.Model):
    name = models.CharField(_('DriveType'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Drive Type')
        verbose_name_plural = _('Drive Types')

class GearBox(models.Model):
    name = models.CharField(_('Gearbox'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Gearbox')
        verbose_name_plural = _('Gearbox')

class Infotainment(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Infotainment')
        verbose_name_plural = _('Infotainments')

class BodyStyle(models.Model):
    style = models.CharField(_('Body Style'), max_length=64)
    note = models.CharField(
        _('Extra Note'),
        max_length=255,
        help_text='(spider/spyder, cabrio/cabriolet, drop/open/soft top)',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.style

    class Meta:
        verbose_name = _('Body Style')
        verbose_name_plural = _('Body Styles')

class Segment(models.Model):
    name = models.CharField(_('Segment Name'), max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Segment')
        verbose_name_plural = _('Segments')

# IMAGE FUNCTIONS
def upload_brand_image(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return '{}/{}/{}.{}'.format('brands', instance.brand_name, 'logo', extension)

def upload_series_image(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return '{}/{}/{}/{}.{}'.format('brands', instance.brand.brand_name, instance.series_name, instance.series_name, extension)

def upload_model_image(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return '{}/{}/{}/{}/{}.{}'.format(
        'brands', 
        instance.series.brand.brand_name,
        instance.series.series_name,
        instance.model_name,
        instance.model_name, 
        extension
    )

# ! MODELS
class Brand(models.Model):
    brand_name = models.CharField(_('Brand Name'), max_length=64)
    brand_slug = models.SlugField(unique=True)
    brand_description=models.TextField(_("Description"), null=True, blank=True)
    
    brand_image = models.ImageField(
        upload_to=upload_brand_image,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    brand_image_url = models.URLField(null=True, blank=True)
    brand_detail_url = models.URLField(_('Main URL'), null=True, blank=True)

    def __str__(self):
        return self.brand_name

    def get_total_series_count(self):
        series = self.brand_series.all().count()
        return series

    def get_continued_count(self):
        series = self.brand_series.filter(series_isDiscontinued=False).count()
        return series

    def get_discontinued_count(self):
        series = self.brand_series.filter(series_isDiscontinued=True).count()
        return series

    @property
    def get_continued_series(self):
        return self.brand_series.filter(series_isDiscontinued=False)

    @property
    def get_discontinued_series(self):
        return self.brand_series.filter(series_isDiscontinued=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

class Series(models.Model):
    series_brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name=_('Brand'),
        related_name='brand_series'
    )
    series_name = models.CharField(_('Series Name'), max_length=255)
    series_slug = models.SlugField()

    series_image = models.ImageField(
        upload_to=upload_series_image,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    series_image_url = models.URLField(null=True, blank=True)

    series_bodyStyle = models.ForeignKey(
        BodyStyle,
        on_delete=models.SET_NULL,
        verbose_name=_('Body Style'),
        null=True,
        blank=True
    )
    series_fuelType = models.ManyToManyField(
        FuelType,
        verbose_name=_('Fuel Type'),
        blank=True
    )

    series_isDiscontinued = models.BooleanField(_('Discontinued Series'), default=False)
    series_generation_count_bot = models.IntegerField(default=0, null=True, blank=True)
    series_detail_url = models.URLField(_('Series Detail Page'), null=True, blank=True)

    def __str__(self):
        return self.series_name

    def get_models_count(self):
        return self.series_models.all().count()

    def get_first_year(self):
        if self.series_models.all().count() > 0:
            model = self.series_models.order_by('model_start_year')[0]
            oldest_year = model.model_start_year
            return oldest_year
        else:
            return None

    def get_last_year(self):
        if self.series_models.all().count() > 0:
            model = self.series_models.order_by('-model_end_year')[0]
            newest_year = model.model_end_year
            return newest_year
        else:
            return None

    @property
    def get_all_models(self):
        return self.series_models.all()

    class Meta:
        verbose_name = _('Series')
        verbose_name_plural = _('Series')


class ModelYear(models.Model):
    year = models.IntegerField(_('Model Year'))

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = _('Year')
        verbose_name_plural = _('Years')

class Model(models.Model):
    model_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('Brand'), related_name='brand_models')
    model_series = models.ForeignKey(Series, on_delete=models.CASCADE, verbose_name=_('Series'), related_name='series_models')
    model_name = models.CharField(_('Model Name'), max_length=255)
    model_slug = models.SlugField()
    model_description=models.TextField(_("Description"), null=True, blank=True)

    # IMAGE
    model_image = models.ImageField(
        upload_to=upload_model_image,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    model_image_url = models.URLField(null=True, blank=True)
    model_image_path = models.CharField(max_length=255, null=True, blank=True)

    # BOT: model_first_year & model_last_year
    model_start_year = models.CharField(_('Start Year'), max_length=4)
    # = Present
    model_end_year = models.CharField(_('End Year'), max_length=8)
    model_years = models.ManyToManyField(ModelYear, verbose_name=_('Model Years'), blank=True)

    model_fuelType = models.ManyToManyField(FuelType, verbose_name=_('Fuel Type'), blank=True)
    model_segment = models.ForeignKey(Segment, on_delete=models.SET_NULL, verbose_name=_('Segment'), null=True, blank=True)
    model_bodyStyle = models.CharField(_('Body Style'), max_length=255, null=True, blank=True)
    model_infotainment = models.ManyToManyField(Infotainment, verbose_name=_('Infotainment'), blank=True)

    model_detail_url = models.URLField(_('Main URL'), null=True, blank=True)

    def __str__(self):
        return self.model_name

    @property
    def get_all_cars(self):
        return self.model_cars.all()
        
    @property
    def get_all_model_images(self):
        return self.images.all()

    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')

class ModelImages(models.Model):
    model = models.ForeignKey(
        Model,
        on_delete=models.CASCADE,
        verbose_name=_('Model Name'),
        related_name='images'
    )
    image_url = models.URLField(_('Image URL'))
    alt_text = models.CharField(_('Alt Text'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.model.model_name

    class Meta:
        verbose_name = _('Model Image')
        verbose_name_plural = _('Model Images')

# CAR
class CarSpecificationType(models.Model):
    name = models.CharField(_('Type Name'), max_length=255, unique=True)
    is_active = models.BooleanField(_('Active'), default=True)

    def __str__(self):
        return self.name

class CarSpecification(models.Model):
    cs_type = models.ForeignKey(
        CarSpecificationType,
        on_delete=models.RESTRICT,
        verbose_name=_('Car Specification Type')
    )
    name = models.CharField(_("Car Specification"), max_length=255, help_text=_("Required"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Car Specification")
        verbose_name_plural = _("Car Specifications")

class Car(models.Model):
    car_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_cars', verbose_name=_('Brand'))
    car_series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='series_cars', verbose_name=_('Series'))
    car_model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_cars', verbose_name=_('Model'))
    car_name = models.CharField(_('Car Name'), max_length=255)
    car_slug = models.SlugField()

    car_fuelType = models.CharField(_('Fuel Type'), max_length=255)
    car_driveType = models.ForeignKey(DriveType, on_delete=models.SET_NULL, verbose_name=_('Drive Type'), null=True, blank=True)
    car_gearBox = models.ForeignKey(GearBox, on_delete=models.SET_NULL, verbose_name=_('Gearbox'), null=True, blank=True)

    car_engine = models.CharField(_('Engine'), max_length=255, null=True, blank=True)
    car_enginePower = models.CharField(_('HP'), max_length=16, null=True, blank=True)

    car_detail_url = models.URLField(_('Main URL'), null=True, blank=True)
    car_alt_url = models.CharField(_('Alt URL'), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.car_name

    @property
    def get_all_specifications(self):
        return self.specifications.all()

class CarSpecificationValue(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="specifications")
    specification = models.ForeignKey(CarSpecification, on_delete=models.RESTRICT, verbose_name=_('Specification'))
    value = models.CharField(_("Value"), max_length=255)

    def __str__(self):
        return f'{self.specification} - {self.value}'

    class Meta:
        verbose_name = _("Car Specification Value")
        verbose_name_plural = _("Car Specification Values")